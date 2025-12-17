from pathlib import Path

from pypdf import PdfReader, PdfWriter

from prism_docs.core.types import OutputConfig
from prism_docs.operations.basic.watermark import WatermarkOperation
from prism_docs.operations.pages.page_numbers import PageNumbersOperation
from prism_docs.operations.pages.reverse import ReverseOperation
from prism_docs.operations.pages.stamp import StampOperation
from prism_docs.operations.utils.crop import CropOperation
from prism_docs.operations.utils.resize import ResizeOperation
from prism_docs.operations.security.flatten import FlattenOperation
from prism_docs.operations.utils.bookmarks import BookmarksOperation
from prism_docs.operations.utils.info import InfoOperation
from tests.helpers import make_pdf


def make_pdf_with_widths(path: Path, widths: list[int]) -> Path:
    writer = PdfWriter()
    for w in widths:
        writer.add_blank_page(width=w, height=200)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        writer.write(f)
    return path


def test_reverse_changes_page_order(tmp_path: Path) -> None:
    src = make_pdf_with_widths(tmp_path / "rev.pdf", [200, 300, 400])
    result = ReverseOperation().execute(src, OutputConfig())
    assert result.success
    reader = PdfReader(result.output_path)
    widths = [float(p.mediabox.width) for p in reader.pages]
    assert widths == [400, 300, 200]


def test_page_numbers_adds_annotations(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "number.pdf", pages=2)
    result = PageNumbersOperation().execute(src, OutputConfig(), format="Pg {n}")
    assert result.success
    reader = PdfReader(result.output_path)
    annots = reader.pages[0].get("/Annots")
    assert annots is not None


def test_stamp_adds_freetext_annotation(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "stamp.pdf")
    result = StampOperation().execute(src, OutputConfig(), text="TEST", position="center")
    assert result.success
    reader = PdfReader(result.output_path)
    annots = reader.pages[0].get("/Annots")
    assert annots is not None


def test_watermark_merges_page(tmp_path: Path) -> None:
    base = make_pdf(tmp_path / "base.pdf", pages=1)
    mark = make_pdf(tmp_path / "mark.pdf", pages=1)
    result = WatermarkOperation().execute(base, OutputConfig(), watermark_path=mark, layer="above")
    assert result.success
    reader = PdfReader(result.output_path)
    assert len(reader.pages) == 1


def test_bookmarks_add_and_extract(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "toc.pdf", pages=2)
    bookmarks = [{"title": "Start", "page": 1}, {"title": "Second", "page": 2}]

    add_result = BookmarksOperation().execute(
        src, OutputConfig(), action="add", bookmarks=bookmarks
    )
    assert add_result.success
    out_pdf = Path(add_result.output_path)
    reader = PdfReader(out_pdf)
    assert reader.outline

    extract_result = BookmarksOperation().execute(out_pdf, OutputConfig(), action="extract")
    assert extract_result.success
    assert extract_result.output_path and extract_result.output_path.exists()
    content = Path(extract_result.output_path).read_text()
    assert "Start" in content and "Second" in content


def test_info_reports_basic_details(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "info.pdf", pages=1)
    result = InfoOperation().execute(src, OutputConfig(), verbose=True)
    assert result.success
    assert "Pages" in result.message


def test_flatten_runs_on_simple_pdf(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "flat.pdf", pages=1)
    result = FlattenOperation().execute(src, OutputConfig())
    assert result.success
    reader = PdfReader(result.output_path)
    assert len(reader.pages) == 1


def test_crop_reduces_margins(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "crop.pdf", pages=1)
    result = CropOperation().execute(src, OutputConfig(), margin=10)
    assert result.success
    reader = PdfReader(result.output_path)
    box = reader.pages[0].mediabox
    assert float(box.width) < 200
    assert float(box.height) < 200


def test_resize_sets_target_size(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "resize.pdf", pages=1)
    result = ResizeOperation().execute(src, OutputConfig(), size="A5")
    assert result.success
    reader = PdfReader(result.output_path)
    box = reader.pages[0].mediabox
    # A5 width ~420, height ~595
    assert 410 < float(box.width) < 430
    assert 585 < float(box.height) < 605
