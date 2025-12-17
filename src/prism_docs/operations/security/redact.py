"""Redact content from PDF."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("redact")
class RedactOperation(BasePDFOperation):
    """Redact (black out) regions of a PDF."""

    @property
    def name(self) -> str:
        return "redact"

    @property
    def description(self) -> str:
        return "Redact (permanently black out) regions of a PDF"

    @property
    def default_suffix(self) -> str:
        return "redacted"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        Add redaction annotations.

        Note: For full redaction (removing underlying text), you need to
        use the 'apply' mode which requires additional processing.
        """
        regions: list[dict] = kwargs.get("regions", [])
        pages: list[int] | None = kwargs.get("pages")
        color: tuple = kwargs.get("color", (0, 0, 0))  # Black

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            writer.add_page(page)

            # Apply redactions to specified pages or all pages
            if pages is not None and (i + 1) not in pages:
                continue

            # Add redaction annotations for each region
            for region in regions:
                x1 = region.get("x1", 0)
                y1 = region.get("y1", 0)
                x2 = region.get("x2", 100)
                y2 = region.get("y2", 100)

                writer.add_annotation(
                    page_number=i,
                    annotation={
                        "/Type": "/Annot",
                        "/Subtype": "/Redact",
                        "/Rect": [x1, y1, x2, y2],
                        "/IC": list(color),  # Interior color
                        "/C": list(color),  # Border color
                        "/F": 4,  # Print flag
                    },
                )

        with open(output_path, "wb") as f:
            writer.write(f)
