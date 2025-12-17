"""Resize PDF pages."""

from pathlib import Path
from typing import Any

from pypdf import PageObject, PdfReader, PdfWriter, Transformation

from prism_docs.core import BasePDFOperation, register_operation

# Standard page sizes in points (72 points = 1 inch)
PAGE_SIZES = {
    "A4": (595.28, 841.89),
    "A3": (841.89, 1190.55),
    "A5": (419.53, 595.28),
    "Letter": (612, 792),
    "Legal": (612, 1008),
    "Tabloid": (792, 1224),
}


@register_operation("resize")
class ResizeOperation(BasePDFOperation):
    """Resize PDF pages to specific dimensions."""

    @property
    def name(self) -> str:
        return "resize"

    @property
    def description(self) -> str:
        return "Resize PDF pages to specific paper size or dimensions"

    @property
    def default_suffix(self) -> str:
        return "resized"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        size: str | None = kwargs.get("size")  # A4, Letter, etc.
        width: float | None = kwargs.get("width")  # In points
        height: float | None = kwargs.get("height")  # In points
        scale: float | None = kwargs.get("scale")  # Scale factor
        fit: str = kwargs.get("fit", "contain")  # contain, cover, stretch
        pages: list[int] | None = kwargs.get("pages")

        # Determine target size
        target_width: float | None
        target_height: float | None
        if size and size.upper() in PAGE_SIZES:
            target_width, target_height = PAGE_SIZES[size.upper()]
        elif width and height:
            target_width, target_height = width, height
        elif scale:
            target_width = target_height = None  # Will calculate per page
        else:
            # Default to A4
            target_width, target_height = PAGE_SIZES["A4"]

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            # Apply resize to specified pages or all pages
            if pages is not None and (i + 1) not in pages:
                writer.add_page(page)
                continue

            media_box = page.mediabox
            current_width = float(media_box.width)
            current_height = float(media_box.height)

            if scale:
                # Simple scaling
                page.scale(scale, scale)
                writer.add_page(page)
            elif target_width is not None and target_height is not None:
                # Resize to target dimensions
                scale_x = target_width / current_width
                scale_y = target_height / current_height

                if fit == "contain":
                    # Fit within target, preserve aspect ratio
                    scale_factor: float | None = min(scale_x, scale_y)
                elif fit == "cover":
                    # Cover target, preserve aspect ratio
                    scale_factor = max(scale_x, scale_y)
                else:
                    # Stretch to fit
                    scale_factor = None

                if scale_factor is not None:
                    # Apply uniform scaling
                    page.scale(scale_factor, scale_factor)

                    # Center on new page if needed
                    new_width = current_width * scale_factor
                    new_height = current_height * scale_factor

                    if fit == "contain":
                        # Create new page with target size and center content
                        new_page = PageObject.create_blank_page(
                            width=target_width, height=target_height
                        )
                        offset_x = (target_width - new_width) / 2
                        offset_y = (target_height - new_height) / 2
                        new_page.merge_transformed_page(
                            page, Transformation().translate(offset_x, offset_y)
                        )
                        writer.add_page(new_page)
                    else:
                        writer.add_page(page)
                else:
                    # Stretch (non-uniform scaling)
                    page.scale(scale_x, scale_y)
                    writer.add_page(page)
            else:
                # No resize needed
                writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
