"""Reverse page order in a PDF."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("reverse")
class ReverseOperation(BasePDFOperation):
    """Reverse the page order of a PDF."""

    @property
    def name(self) -> str:
        return "reverse"

    @property
    def description(self) -> str:
        return "Reverse the page order of a PDF"

    @property
    def default_suffix(self) -> str:
        return "reversed"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Add pages in reverse order
        for page in reversed(reader.pages):
            writer.add_page(page)

        # Copy metadata
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        with open(output_path, "wb") as f:
            writer.write(f)
