from pathlib import Path

from prism_docs.core.types import OutputConfig
from prism_docs.operations.security.permissions import PermissionsOperation
from prism_docs.operations.utils.validate import ValidateOperation
from .helpers import make_pdf


def test_validate_passes_on_good_pdf(tmp_path: Path) -> None:
    pdf = make_pdf(tmp_path / "valid.pdf")

    result = ValidateOperation().execute(pdf, OutputConfig())  # OutputConfig unused
    assert result.success
    assert "valid" in result.message


def test_validate_flags_encrypted_pdf(tmp_path: Path) -> None:
    pdf = make_pdf(tmp_path / "encrypted.pdf")

    # Encrypt using the permissions operation to stay consistent
    encrypted = PermissionsOperation().execute(
        pdf,
        OutputConfig(),  # OutputConfig unused in permissions execute override
        user_password="pwd",
    )
    assert encrypted.output_path is not None

    result = ValidateOperation().execute(encrypted.output_path, OutputConfig())
    assert not result.success
    assert "encrypted" in result.message
