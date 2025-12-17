"""OCR PDF pages to extract text."""

from pathlib import Path
from typing import Any

import pytesseract
from pdf2image import convert_from_path

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("ocr")
class OCRPDFOperation(BasePDFOperation):
    """Extract text from scanned PDF using OCR."""

    @property
    def name(self) -> str:
        return "ocr"

    @property
    def description(self) -> str:
        return "Extract text from scanned PDF using Tesseract OCR"

    @property
    def default_suffix(self) -> str:
        return "ocr"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        OCR a PDF and save extracted text.

        Args:
            input_path: Path to input PDF
            output_path: Path to output text file
            lang: OCR language(s) (default: eng)
            dpi: DPI for PDF to image conversion (default: 300)
            psm: Page segmentation mode (default: 3)
            oem: OCR engine mode (default: 3)
            config: Additional Tesseract config string
            pages: Specific pages to OCR (default: all)
            timeout: Timeout per page in seconds (default: 30)
        """
        lang = kwargs.get("lang", "eng")
        dpi = kwargs.get("dpi", 300)
        psm = kwargs.get("psm", 3)
        oem = kwargs.get("oem", 3)
        extra_config = kwargs.get("config", "")
        pages = kwargs.get("pages")
        timeout = kwargs.get("timeout", 30)

        # Build Tesseract config
        tess_config = f"--psm {psm} --oem {oem}"
        if extra_config:
            tess_config = f"{tess_config} {extra_config}"

        # Convert PDF to images
        if pages:
            images = convert_from_path(
                input_path,
                dpi=dpi,
                first_page=pages[0],
                last_page=pages[-1],
            )
        else:
            images = convert_from_path(input_path, dpi=dpi)

        # OCR each page
        text_parts: list[str] = []
        for i, image in enumerate(images, start=1):
            page_text = pytesseract.image_to_string(
                image,
                lang=lang,
                config=tess_config,
                timeout=timeout,
            )
            text_parts.append(f"--- Page {i} ---\n{page_text}")

        # Write output
        output_path = output_path.with_suffix(".txt")
        output_path.write_text("\n\n".join(text_parts), encoding="utf-8")
