"""Add text stamps to PDF pages."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("stamp")
class StampOperation(BasePDFOperation):
    """Add a text stamp to PDF pages."""

    @property
    def name(self) -> str:
        return "stamp"

    @property
    def description(self) -> str:
        return "Add text stamp (e.g., CONFIDENTIAL, DRAFT) to PDF pages"

    @property
    def default_suffix(self) -> str:
        return "stamped"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        text: str = kwargs.get("text", "CONFIDENTIAL")
        position: str = kwargs.get("position", "top-right")
        font_size: int = kwargs.get("font_size", 24)
        color: str = kwargs.get("color", "red")
        opacity: float = kwargs.get("opacity", 0.5)
        pages: list[int] | None = kwargs.get("pages")
        margin: int = kwargs.get("margin", 36)

        # Color mapping (RGB values 0-1)
        colors = {
            "red": (1, 0, 0),
            "blue": (0, 0, 1),
            "green": (0, 0.5, 0),
            "black": (0, 0, 0),
            "gray": (0.5, 0.5, 0.5),
        }
        r, g, b = colors.get(color, colors["red"])

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            writer.add_page(page)

            # Apply stamp to specified pages or all pages
            if pages is not None and (i + 1) not in pages:
                continue

            # Get page dimensions
            media_box = page.mediabox
            page_width = float(media_box.width)
            page_height = float(media_box.height)

            # Calculate position
            x, y = self._calculate_position(
                position, page_width, page_height, margin, font_size, len(text)
            )

            # Add stamp as annotation
            writer.add_annotation(
                page_number=i,
                annotation={
                    "/Type": "/Annot",
                    "/Subtype": "/FreeText",
                    "/Rect": [
                        x - 10,
                        y - 5,
                        x + len(text) * font_size * 0.6 + 10,
                        y + font_size + 5,
                    ],
                    "/Contents": text,
                    "/DA": f"/Helv {font_size} Tf {r} {g} {b} rg",
                    "/F": 4,  # Print flag
                    "/CA": opacity,
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
        """Calculate x, y coordinates for stamp."""
        text_width = text_len * font_size * 0.6

        positions = {
            "top-left": (margin, page_height - margin - font_size),
            "top-center": ((page_width - text_width) / 2, page_height - margin - font_size),
            "top-right": (page_width - margin - text_width, page_height - margin - font_size),
            "center": ((page_width - text_width) / 2, (page_height - font_size) / 2),
            "bottom-left": (margin, margin),
            "bottom-center": ((page_width - text_width) / 2, margin),
            "bottom-right": (page_width - margin - text_width, margin),
        }

        return positions.get(position, positions["top-right"])
