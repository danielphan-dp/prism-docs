"""Crop PDF pages."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("crop")
class CropOperation(BasePDFOperation):
    """Crop PDF page margins."""

    @property
    def name(self) -> str:
        return "crop"

    @property
    def description(self) -> str:
        return "Crop PDF page margins"

    @property
    def default_suffix(self) -> str:
        return "cropped"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        # Margins to remove (in points, 72 points = 1 inch)
        left: float = kwargs.get("left", 0)
        right: float = kwargs.get("right", 0)
        top: float = kwargs.get("top", 0)
        bottom: float = kwargs.get("bottom", 0)

        # Or use uniform margin
        margin: float | None = kwargs.get("margin")
        if margin is not None:
            left = right = top = bottom = margin

        # Or use percentage
        percent: float | None = kwargs.get("percent")

        pages: list[int] | None = kwargs.get("pages")

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            # Apply crop to specified pages or all pages
            if pages is None or (i + 1) in pages:
                media_box = page.mediabox
                width = float(media_box.width)
                height = float(media_box.height)

                # Calculate crop values
                if percent is not None:
                    crop_left = width * percent / 100
                    crop_right = width * percent / 100
                    crop_top = height * percent / 100
                    crop_bottom = height * percent / 100
                else:
                    crop_left = left
                    crop_right = right
                    crop_top = top
                    crop_bottom = bottom

                # Apply crop
                page.mediabox.lower_left = (
                    float(media_box.lower_left[0]) + crop_left,
                    float(media_box.lower_left[1]) + crop_bottom,
                )
                page.mediabox.upper_right = (
                    float(media_box.upper_right[0]) - crop_right,
                    float(media_box.upper_right[1]) - crop_top,
                )

            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
