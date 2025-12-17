"""Add page numbers to PDF pages."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("page-numbers")
class PageNumbersOperation(BasePDFOperation):
    """Add page numbers to all pages of a PDF."""

    @property
    def name(self) -> str:
        return "page-numbers"

    @property
    def description(self) -> str:
        return "Add page numbers to PDF pages"

    @property
    def default_suffix(self) -> str:
        return "numbered"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        position: str = kwargs.get("position", "bottom-center")
        start_number: int = kwargs.get("start_number", 1)
        format_str: str = kwargs.get("format", "Page {n}")
        font_size: int = kwargs.get("font_size", 12)
        margin: int = kwargs.get("margin", 36)  # points from edge
        skip_first: bool = kwargs.get("skip_first", False)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            page_num = start_number + i

            if skip_first and i == 0:
                writer.add_page(page)
                continue

            # Get page dimensions
            media_box = page.mediabox
            page_width = float(media_box.width)
            page_height = float(media_box.height)

            # Calculate position
            text = format_str.format(n=page_num, total=len(reader.pages))
            x, y = self._calculate_position(
                position, page_width, page_height, margin, font_size, len(text)
            )

            # Add the page number as annotation
            writer.add_page(page)

            # Add annotation for page number
            writer.add_annotation(
                page_number=i,
                annotation={
                    "/Type": "/Annot",
                    "/Subtype": "/FreeText",
                    "/Rect": [x - 50, y - 5, x + 100, y + font_size + 5],
                    "/Contents": text,
                    "/DA": f"/Helv {font_size} Tf 0 g",
                    "/F": 4,  # Print flag
                },
            )

        with open(output_path, "wb") as f:
            writer.write(f)

    def _calculate_position(
        self,
        position: str,
        page_width: float,
        page_height: float,
        margin: int,
        font_size: int,
        text_len: int,
    ) -> tuple[float, float]:
        """Calculate x, y coordinates for page number."""
        # Approximate text width (rough estimate)
        text_width = text_len * font_size * 0.5

        positions = {
            "bottom-left": (margin, margin),
            "bottom-center": ((page_width - text_width) / 2, margin),
            "bottom-right": (page_width - margin - text_width, margin),
            "top-left": (margin, page_height - margin - font_size),
            "top-center": ((page_width - text_width) / 2, page_height - margin - font_size),
            "top-right": (page_width - margin - text_width, page_height - margin - font_size),
        }

        return positions.get(position, positions["bottom-center"])
