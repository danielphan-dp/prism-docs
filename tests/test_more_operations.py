from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject

from prism_docs.core.types import OutputConfig, OverwritePolicy
from prism_docs.operations.basic.merge import MergeOperation
from prism_docs.operations.pages.extract_text import ExtractTextOperation
from prism_docs.operations.pages.interleave import InterleaveOperation
from prism_docs.operations.pages.overlay import OverlayOperation
from prism_docs.operations.pages.split import SplitOperation
from prism_docs.operations.security.flatten import FlattenOperation
from prism_docs.operations.security.redact import RedactOperation
from prism_docs.operations.utils.bookmarks import BookmarksOperation
from prism_docs.operations.utils.info import InfoOperation
from tests.helpers import make_pdf


def test_split_ranges(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "ranges.pdf", pages=5)
    result = SplitOperation().execute(src, OutputConfig(), mode="ranges", ranges=[(1, 2), (3, 5)])
    assert result.success
    assert (tmp_path / "ranges_part_1.pdf").exists()
    assert (tmp_path / "ranges_part_2.pdf").exists()


def test_overlay_background_nonrepeat(tmp_path: Path) -> None:
    base = make_pdf(tmp_path / "base.pdf", pages=2)
    overlay = make_pdf(tmp_path / "overlay.pdf", pages=1)
    result = OverlayOperation().execute(
        base,
        OutputConfig(),
        overlay_path=overlay,
        mode="background",
        repeat=False,
        pages=[1],
    )
    assert result.success
    reader = PdfReader(result.output_path)
    assert len(reader.pages) == 2


def test_interleave_front_back_pattern(tmp_path: Path) -> None:
    a = make_pdf(tmp_path / "front.pdf", pages=1)
    b = make_pdf(tmp_path / "back.pdf", pages=1)
    result = InterleaveOperation().execute(a, OutputConfig(), second_path=b, pattern="front-back")
    assert result.success
    reader = PdfReader(result.output_path)
    assert len(reader.pages) == 2


def test_extract_text_handles_pages_list(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "text.pdf", pages=2)
    out = tmp_path / "text.txt"
    result = ExtractTextOperation().execute(src, OutputConfig(), pages=[1], output_path=out)
    assert result.success
    assert out.exists()
    content = out.read_text()
    assert content == ""


def test_redact_adds_annotations(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "redact.pdf", pages=1)
    result = RedactOperation().execute(
        src,
        OutputConfig(),
        regions=[{"x1": 0, "y1": 0, "x2": 50, "y2": 50}],
        pages=[1],
    )
    assert result.success
    reader = PdfReader(result.output_path)
    annots = reader.pages[0].get("/Annots")
    assert annots is not None


def _pdf_with_form(path: Path) -> Path:
    writer = PdfWriter()
    page = writer.add_blank_page(width=200, height=200)

    widget = DictionaryObject()
    widget.update(
        {
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/Ff"): NumberObject(0),
        }
    )
    widget_ref = writer._add_object(widget)
    page[NameObject("/Annots")] = ArrayObject([widget_ref])

    writer._root_object.update({NameObject("/AcroForm"): DictionaryObject()})

    with open(path, "wb") as f:
        writer.write(f)
    return path


def test_flatten_sets_widget_readonly(tmp_path: Path) -> None:
    src = _pdf_with_form(tmp_path / "form.pdf")
    result = FlattenOperation().execute(src, OutputConfig(), forms=True)
    assert result.success
    reader = PdfReader(result.output_path)
    page = reader.pages[0]
    annots = page.get("/Annots")
    assert annots is not None
    annot_obj = annots[0].get_object()
    assert annot_obj.get("/Ff") == 1


def test_bookmarks_view_and_from_file(tmp_path: Path) -> None:
    # No bookmarks path
    empty = make_pdf(tmp_path / "nobook.pdf", pages=1)
    view = BookmarksOperation().execute(empty, OutputConfig(), action="view")
    assert view.success
    assert "no bookmarks" in view.message.lower()

    # Load from file then add/extract
    src = make_pdf(tmp_path / "book.pdf", pages=1)
    txt = tmp_path / "bookmarks.txt"
    txt.write_text("Intro|1\n")
    add = BookmarksOperation().execute(
        src,
        OutputConfig(),
        action="add",
        from_file=txt,
    )
    assert add.success
    extract = BookmarksOperation().execute(Path(add.output_path), OutputConfig(), action="extract")
    assert extract.success
    assert extract.output_path and Path(extract.output_path).exists()
    assert "Intro" in Path(extract.output_path).read_text()


def test_info_json_includes_metadata(tmp_path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.add_metadata({"/Title": "T", "/Author": "A"})
    path = tmp_path / "meta.pdf"
    with open(path, "wb") as f:
        writer.write(f)

    result = InfoOperation().execute(path, OutputConfig(), json=True)
    assert result.success
    assert '"title": "T"' in result.message or '"title": "T"' in result.message.lower()


def test_merge_uses_custom_output(tmp_path: Path) -> None:
    a = make_pdf(tmp_path / "ma.pdf")
    b = make_pdf(tmp_path / "mb.pdf")
    out = tmp_path / "out.pdf"
    result = MergeOperation().execute(a, OutputConfig(), merge_inputs=[a, b], output_path=out)
    assert result.success
    assert result.output_path == out
