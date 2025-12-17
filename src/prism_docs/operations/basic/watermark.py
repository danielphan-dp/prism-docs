"""Watermark PDF operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("watermark")
class WatermarkOperation(BasePDFOperation):
    """Add a watermark to all pages of a PDF."""

    @property
    def name(self) -> str:
        return "watermark"

    @property
    def description(self) -> str:
        return "Add a watermark to all pages of a PDF"

    @property
    def default_suffix(self) -> str:
        return "watermarked"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        watermark_path: Path = Path(kwargs["watermark_path"])
        pages: list[int] | None = kwargs.get("pages")  # None = all pages
        layer: str = kwargs.get("layer", "below")  # "below" or "above"

        watermark_reader = PdfReader(watermark_path)
        watermark_page = watermark_reader.pages[0]

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            # Apply watermark to specified pages or all pages
            if pages is None or (i + 1) in pages:
                if layer == "below":
                    # Watermark below content
                    watermark_copy = watermark_reader.pages[0]
                    watermark_copy.merge_page(page)
                    writer.add_page(watermark_copy)
                else:
                    # Watermark above content
                    page.merge_page(watermark_page)
                    writer.add_page(page)
            else:
                writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
