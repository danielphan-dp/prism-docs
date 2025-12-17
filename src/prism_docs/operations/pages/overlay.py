"""Overlay one PDF on another."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("overlay")
class OverlayOperation(BasePDFOperation):
    """Overlay one PDF on another (more flexible than watermark)."""

    @property
    def name(self) -> str:
        return "overlay"

    @property
    def description(self) -> str:
        return "Overlay one PDF on another (background or foreground)"

    @property
    def default_suffix(self) -> str:
        return "overlay"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        overlay_path: Path = Path(kwargs["overlay_path"])
        mode: str = kwargs.get("mode", "foreground")  # foreground or background
        pages: list[int] | None = kwargs.get("pages")  # None = all pages
        repeat: bool = kwargs.get("repeat", True)  # Repeat overlay for all pages

        overlay_reader = PdfReader(overlay_path)
        overlay_pages = list(overlay_reader.pages)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            # Determine which overlay page to use
            if repeat:
                overlay_page = overlay_pages[i % len(overlay_pages)]
            elif i < len(overlay_pages):
                overlay_page = overlay_pages[i]
            else:
                overlay_page = None

            # Apply overlay to specified pages or all pages
            if overlay_page and (pages is None or (i + 1) in pages):
                if mode == "background":
                    # Overlay as background (under content)
                    overlay_copy = overlay_reader.pages[i % len(overlay_pages)]
                    overlay_copy.merge_page(page)
                    writer.add_page(overlay_copy)
                else:
                    # Overlay as foreground (over content)
                    page.merge_page(overlay_page)
                    writer.add_page(page)
            else:
                writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
