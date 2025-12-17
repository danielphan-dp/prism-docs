"""Extract pages from PDF operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("extract-pages")
class ExtractPagesOperation(BasePDFOperation):
    """Extract a range of pages from a PDF."""

    @property
    def name(self) -> str:
        return "extract-pages"

    @property
    def description(self) -> str:
        return "Extract a range of pages from a PDF (1-indexed, inclusive)"

    @property
    def default_suffix(self) -> str:
        return "extracted"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        start: int = kwargs.get("start", 1)
        end: int | None = kwargs.get("end")
        pages: list[int] | None = kwargs.get("pages")  # Specific pages to extract

        reader = PdfReader(input_path)
        writer = PdfWriter()

        total_pages = len(reader.pages)

        if pages is not None:
            # Extract specific pages
            for page_num in pages:
                if 1 <= page_num <= total_pages:
                    writer.add_page(reader.pages[page_num - 1])
        else:
            # Extract range
            if end is None:
                end = total_pages

            for i in range(start - 1, min(end, total_pages)):
                writer.add_page(reader.pages[i])

        with open(output_path, "wb") as f:
            writer.write(f)
