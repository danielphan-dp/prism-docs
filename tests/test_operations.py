from pathlib import Path

from pypdf import PdfReader

from prism_docs.core.types import OutputConfig, OverwritePolicy
from prism_docs.operations.basic.compress import CompressOperation
from prism_docs.operations.basic.merge import MergeOperation
from prism_docs.operations.basic.metadata import MetadataOperation
from prism_docs.operations.pages.extract_pages import ExtractPagesOperation
from prism_docs.operations.pages.interleave import InterleaveOperation
from prism_docs.operations.pages.overlay import OverlayOperation
from prism_docs.operations.pages.remove_pages import RemovePagesOperation
from prism_docs.operations.pages.rotate import RotateOperation
from prism_docs.operations.pages.split import SplitOperation
from prism_docs.operations.security.permissions import PermissionsOperation
from .helpers import make_pdf


def test_merge_operation_merges_multiple_files(tmp_path: Path) -> None:
    first = make_pdf(tmp_path / "a.pdf")
    second = make_pdf(tmp_path / "b.pdf")
    out = tmp_path / "merged.pdf"

    result = MergeOperation().execute(
        first,
        OutputConfig(),
        merge_inputs=[first, second],
        output_path=out,
    )

    assert result.success
    reader = PdfReader(out)
    assert len(reader.pages) == 2


def test_split_into_pages(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "multi.pdf", pages=3)

    result = SplitOperation().execute(src, OutputConfig())
    assert result.success

    # Three separate files should be created
    for i in range(1, 4):
        part = src.with_name(f"{src.stem}_page_{i}.pdf")
        assert part.exists()

    first_out = src.with_name(f"{src.stem}_page_1.pdf")
    reader = PdfReader(first_out)
    assert len(reader.pages) == 1


def test_extract_pages_by_range_and_list(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "extract.pdf", pages=5)

    range_result = ExtractPagesOperation().execute(src, OutputConfig(), start=2, end=4)
    assert range_result.success
    range_reader = PdfReader(range_result.output_path)
    assert len(range_reader.pages) == 3

    list_result = ExtractPagesOperation().execute(src, OutputConfig(), pages=[1, 5])
    assert list_result.success
    list_reader = PdfReader(list_result.output_path)
    assert len(list_reader.pages) == 2


def test_compress_preserves_metadata(tmp_path: Path) -> None:
    meta = {"/Title": "Example", "/Author": "Tester"}
    src = make_pdf(tmp_path / "src.pdf", metadata=meta)
    out = tmp_path / "compressed.pdf"

    result = CompressOperation().execute(src, OutputConfig(), output_path=out)

    assert result.success
    reader = PdfReader(out)
    assert reader.metadata.get("/Title") == "Example"
    assert reader.metadata.get("/Author") == "Tester"
    assert len(reader.pages) == 1


def test_interleave_creates_expected_page_count(tmp_path: Path) -> None:
    first = make_pdf(tmp_path / "front.pdf", pages=2)
    second = make_pdf(tmp_path / "back.pdf", pages=2)
    out = tmp_path / "interleaved.pdf"

    result = InterleaveOperation().execute(
        first,
        OutputConfig(),
        second_path=second,
        output_path=out,
    )

    assert result.success
    reader = PdfReader(out)
    assert len(reader.pages) == 4


def test_rotate_specific_pages(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "rotate.pdf", pages=2)

    result = RotateOperation().execute(src, OutputConfig(), degrees=180, pages=[2])

    assert result.success
    reader = PdfReader(result.output_path)
    assert reader.pages[0].get("/Rotate", 0) in (0, None)
    assert reader.pages[1].get("/Rotate", 0) == 180


def test_metadata_edit_and_view(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "meta.pdf")

    # Edit metadata
    edit_result = MetadataOperation().execute(
        src,
        OutputConfig(),
        action="edit",
        title="Example",
        author="Author",
    )
    assert edit_result.success
    assert edit_result.output_path and edit_result.output_path.exists()

    reader = PdfReader(edit_result.output_path)
    assert reader.metadata.get("/Title") == "Example"
    assert reader.metadata.get("/Author") == "Author"

    # View metadata
    view_result = MetadataOperation().execute(src, OutputConfig(), action="view")
    assert view_result.success
    assert "Metadata for" in view_result.message


def test_permissions_encrypts_pdf(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "restricted.pdf")

    result = PermissionsOperation().execute(
        src,
        OutputConfig(),
        user_password="user",
        owner_password="owner",
        copy=False,
        print=False,
    )

    assert result.success
    assert result.output_path is not None

    reader = PdfReader(result.output_path)
    assert reader.is_encrypted
    assert reader.decrypt("user")  # should decrypt with user password
    assert len(reader.pages) == 1


def test_remove_pages_drops_requested(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "remove.pdf", pages=4)

    result = RemovePagesOperation().execute(src, OutputConfig(), pages=[2, 4])
    assert result.success
    reader = PdfReader(result.output_path)
    assert len(reader.pages) == 2


def test_overlay_repeats_foreground(tmp_path: Path) -> None:
    base = make_pdf(tmp_path / "base.pdf", pages=2)
    overlay = make_pdf(tmp_path / "overlay.pdf", pages=1)

    result = OverlayOperation().execute(
        base, OutputConfig(), overlay_path=overlay, mode="foreground", repeat=True
    )

    assert result.success
    reader = PdfReader(result.output_path)
    assert len(reader.pages) == 2


def test_output_config_rename_policy(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "doc.pdf")

    # Prepare existing output to trigger rename
    out_config = OutputConfig(overwrite=OverwritePolicy.RENAME)
    initial_out = out_config.resolve_output_path(src, "compressed")
    initial_out.parent.mkdir(parents=True, exist_ok=True)
    initial_out.touch()

    result = CompressOperation().execute(src, out_config)
    assert result.success
    assert result.output_path is not None
    assert result.output_path != initial_out
    assert result.output_path.exists()
