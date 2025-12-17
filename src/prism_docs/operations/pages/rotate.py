"""Rotate PDF pages operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("rotate")
class RotateOperation(BasePDFOperation):
    """Rotate pages in a PDF."""

    @property
    def name(self) -> str:
        return "rotate"

    @property
    def description(self) -> str:
        return "Rotate pages in a PDF (90, 180, or 270 degrees)"

    @property
    def default_suffix(self) -> str:
        return "rotated"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        degrees: int = kwargs.get("degrees", 90)
        pages: list[int] | None = kwargs.get("pages")  # None = all pages

        if degrees not in (90, 180, 270):
            raise ValueError(f"Rotation must be 90, 180, or 270 degrees, got {degrees}")

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if pages is None or (i + 1) in pages:
                page.rotate(degrees)
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
