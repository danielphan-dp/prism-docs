"""Create searchable PDF from scanned PDF using OCR."""

from pathlib import Path
from typing import Any

import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("searchable-pdf")
class SearchablePDFOperation(BasePDFOperation):
    """Create searchable PDF with OCR text layer."""

    @property
    def name(self) -> str:
        return "searchable-pdf"

    @property
    def description(self) -> str:
        return "Create searchable PDF by adding OCR text layer"

    @property
    def default_suffix(self) -> str:
        return "searchable"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        Create searchable PDF with invisible text layer.

        Args:
            input_path: Path to input scanned PDF
            output_path: Path to output searchable PDF
            lang: OCR language(s) (default: eng)
            dpi: DPI for conversion (default: 300)
            psm: Page segmentation mode (default: 3)
            oem: OCR engine mode (default: 3)
            timeout: Timeout per page in seconds (default: 60)
        """
        lang = kwargs.get("lang", "eng")
        dpi = kwargs.get("dpi", 300)
        psm = kwargs.get("psm", 3)
        oem = kwargs.get("oem", 3)
        timeout = kwargs.get("timeout", 60)

        tess_config = f"--psm {psm} --oem {oem}"

        # Convert PDF to images
        images = convert_from_path(input_path, dpi=dpi)

        # Generate PDF with text layer for each page
        pdf_pages: list[bytes] = []
        for image in images:
            # Get PDF bytes with invisible text layer
            pdf_result = pytesseract.image_to_pdf_or_hocr(
                image,
                lang=lang,
                config=tess_config,
                timeout=timeout,
                extension="pdf",
            )
            pdf_bytes = pdf_result if isinstance(pdf_result, bytes) else pdf_result.encode()
            pdf_pages.append(pdf_bytes)

        # Merge all pages into single PDF
        writer = PdfWriter()
        for pdf_bytes in pdf_pages:
            from io import BytesIO

            reader = PdfReader(BytesIO(pdf_bytes))
            for page in reader.pages:
                writer.add_page(page)

        # Write output
        with open(output_path, "wb") as f:
            writer.write(f)
