"""Remove pages from a PDF."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("remove-pages")
class RemovePagesOperation(BasePDFOperation):
    """Remove specific pages from a PDF."""

    @property
    def name(self) -> str:
        return "remove-pages"

    @property
    def description(self) -> str:
        return "Remove specific pages from a PDF"

    @property
    def default_suffix(self) -> str:
        return "trimmed"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        pages_to_remove: list[int] = kwargs.get("pages", [])

        if not pages_to_remove:
            raise ValueError("No pages specified to remove")

        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Convert to set for O(1) lookup, adjust to 0-indexed
        remove_set = {p - 1 for p in pages_to_remove}

        for i, page in enumerate(reader.pages):
            if i not in remove_set:
                writer.add_page(page)

        # Copy metadata
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        with open(output_path, "wb") as f:
            writer.write(f)
