"""Validate PDF files."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("validate")
class ValidateOperation(BasePDFOperation):
    """Validate PDF file integrity."""

    @property
    def name(self) -> str:
        return "validate"

    @property
    def description(self) -> str:
        return "Validate PDF file integrity and report issues"

    @property
    def default_suffix(self) -> str:
        return ""

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override to validate without creating output file."""
        input_path = Path(input_path)

        try:
            issues = self._validate(input_path, **kwargs)

            if issues:
                return OperationResult(
                    success=False,
                    input_path=input_path,
                    message=f"Validation failed for '{input_path}':\n"
                    + "\n".join(f"  - {i}" for i in issues),
                )
            else:
                return OperationResult(
                    success=True,
                    input_path=input_path,
                    message=f"'{input_path}' is valid",
                )

        except PdfReadError as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"'{input_path}' is corrupted or invalid: {e}",
                error=e,
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to validate '{input_path}': {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see execute override."""
        pass

    def _validate(self, input_path: Path, **kwargs: Any) -> list[str]:
        strict: bool = kwargs.get("strict", False)
        issues = []

        # Try to read the PDF
        reader = PdfReader(input_path, strict=strict)

        # Check page count
        if len(reader.pages) == 0:
            issues.append("PDF has no pages")

        # Try to read each page
        for i, page in enumerate(reader.pages):
            try:
                # Try to access page content
                _ = page.mediabox
            except Exception as e:
                issues.append(f"Page {i + 1}: Unable to read - {e}")

        # Check for encryption issues
        if reader.is_encrypted:
            try:
                # Check if we can decrypt with empty password
                reader.decrypt("")
            except Exception:
                issues.append("PDF is encrypted and requires a password")

        return issues
