"""Batch OCR processing for multiple PDFs."""

from pathlib import Path
from typing import Any

import pytesseract
from pdf2image import convert_from_path

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("ocr-batch")
class BatchOCROperation(BasePDFOperation):
    """Batch OCR multiple PDFs with consistent settings."""

    @property
    def name(self) -> str:
        return "ocr-batch"

    @property
    def description(self) -> str:
        return "Batch OCR multiple PDFs with consistent settings"

    @property
    def default_suffix(self) -> str:
        return "ocr"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        OCR a single PDF (batch handled by runner).

        Args:
            input_path: Path to input PDF
            output_path: Path to output
            lang: OCR language(s) (default: eng)
            dpi: DPI for conversion (default: 200 for speed)
            psm: Page segmentation mode (default: 3)
            output_type: Output type: txt, pdf (default: txt)
            fast: Use fast mode with lower DPI (default: False)
        """
        lang = kwargs.get("lang", "eng")
        fast = kwargs.get("fast", False)
        dpi = kwargs.get("dpi", 150 if fast else 300)
        psm = kwargs.get("psm", 3)
        output_type = kwargs.get("output_type", "txt")

        tess_config = f"--psm {psm} --oem 3"
        if fast:
            tess_config = f"{tess_config} -c tessedit_do_invert=0"

        images = convert_from_path(input_path, dpi=dpi)

        if output_type == "pdf":
            # Create searchable PDF
            from io import BytesIO

            from pypdf import PdfReader, PdfWriter

            writer = PdfWriter()
            for image in images:
                pdf_result = pytesseract.image_to_pdf_or_hocr(
                    image, lang=lang, config=tess_config, extension="pdf"
                )
                pdf_bytes = pdf_result if isinstance(pdf_result, bytes) else pdf_result.encode()
                reader = PdfReader(BytesIO(pdf_bytes))
                for page in reader.pages:
                    writer.add_page(page)

            with open(output_path, "wb") as f:
                writer.write(f)
        else:
            # Extract text
            text_parts = []
            for i, image in enumerate(images, start=1):
                text = pytesseract.image_to_string(image, lang=lang, config=tess_config)
                text_parts.append(f"--- Page {i} ---\n{text}")

            output_path = output_path.with_suffix(".txt")
            output_path.write_text("\n\n".join(text_parts), encoding="utf-8")
