from pathlib import Path

from prism_docs.core.types import OutputConfig, OutputNaming, OverwritePolicy


def test_suffix_naming_default(tmp_path: Path) -> None:
    cfg = OutputConfig()
    input_path = tmp_path / "doc.pdf"
    out = cfg.resolve_output_path(input_path, "compressed")
    assert out.name == "doc-compressed.pdf"


def test_prefix_naming(tmp_path: Path) -> None:
    cfg = OutputConfig(naming=OutputNaming.PREFIX, prefix="new-")
    input_path = tmp_path / "doc.pdf"
    out = cfg.resolve_output_path(input_path, "ignored")
    assert out.name == "new-doc.pdf"


def test_custom_pattern(tmp_path: Path) -> None:
    cfg = OutputConfig(naming=OutputNaming.CUSTOM, pattern="{prefix}{stem}{suffix}{ext}")
    cfg.prefix = "p-"
    cfg.suffix = "-s"
    input_path = tmp_path / "doc.pdf"
    out = cfg.resolve_output_path(input_path, "ignored")
    assert out.name == "p-doc-s.pdf"


def test_rename_policy_increments(tmp_path: Path) -> None:
    cfg = OutputConfig(overwrite=OverwritePolicy.RENAME)
    input_path = tmp_path / "doc.pdf"
    first = cfg.resolve_output_path(input_path, "compressed")
    first.parent.mkdir(parents=True, exist_ok=True)
    first.touch()

    second = cfg.resolve_output_path(input_path, "compressed")
    assert second != first
    assert second.name.startswith("doc-compressed")


def test_skip_and_error_policies(tmp_path: Path) -> None:
    target = tmp_path / "f.pdf"
    target.touch()

    skip_cfg = OutputConfig(overwrite=OverwritePolicy.SKIP)
    import pytest

    with pytest.raises(FileExistsError):
        skip_cfg.resolve_output_path(target, "x")

    error_cfg = OutputConfig(overwrite=OverwritePolicy.ERROR)
    with pytest.raises(FileExistsError):
        error_cfg.resolve_output_path(target, "x")
