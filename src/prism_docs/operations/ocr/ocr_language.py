"""OCR language detection and multi-language support."""

from pathlib import Path
from typing import Any

import pytesseract
from pdf2image import convert_from_path

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("ocr-detect-lang")
class OCRDetectLanguageOperation(BasePDFOperation):
    """Detect language in PDF and OCR with appropriate settings."""

    @property
    def name(self) -> str:
        return "ocr-detect-lang"

    @property
    def description(self) -> str:
        return "Detect language in PDF and perform OCR"

    @property
    def default_suffix(self) -> str:
        return "ocr"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        Auto-detect language and OCR.

        Args:
            input_path: Path to input PDF
            output_path: Path to output text file
            dpi: DPI for conversion (default: 300)
            fallback_lang: Fallback language if detection fails (default: eng)
            sample_pages: Number of pages to sample for detection (default: 1)
        """
        dpi = kwargs.get("dpi", 300)
        fallback_lang = kwargs.get("fallback_lang", "eng")
        sample_pages = kwargs.get("sample_pages", 1)

        # Convert first few pages for language detection
        images = convert_from_path(input_path, dpi=dpi, last_page=sample_pages)

        # Detect language using OSD
        detected_lang = fallback_lang
        try:
            for image in images[:sample_pages]:
                osd = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
                script = osd.get("script", "").lower()

                # Map script to Tesseract language code
                script_lang_map = {
                    "latin": "eng",
                    "cyrillic": "rus",
                    "arabic": "ara",
                    "hebrew": "heb",
                    "han": "chi_sim",
                    "hangul": "kor",
                    "hiragana": "jpn",
                    "katakana": "jpn",
                    "thai": "tha",
                    "devanagari": "hin",
                    "greek": "ell",
                }
                detected_lang = script_lang_map.get(script, fallback_lang)
                break
        except pytesseract.TesseractError:
            detected_lang = fallback_lang

        # Now OCR all pages with detected language
        all_images = convert_from_path(input_path, dpi=dpi)

        text_parts = [f"Detected language: {detected_lang}\n"]
        for i, image in enumerate(all_images, start=1):
            text = pytesseract.image_to_string(image, lang=detected_lang)
            text_parts.append(f"--- Page {i} ---\n{text}")

        output_path = output_path.with_suffix(".txt")
        output_path.write_text("\n\n".join(text_parts), encoding="utf-8")


@register_operation("ocr-multi-lang")
class OCRMultiLanguageOperation(BasePDFOperation):
    """OCR with multiple languages simultaneously."""

    @property
    def name(self) -> str:
        return "ocr-multi-lang"

    @property
    def description(self) -> str:
        return "OCR with multiple languages for mixed-language documents"

    @property
    def default_suffix(self) -> str:
        return "ocr"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        OCR with multiple languages.

        Args:
            input_path: Path to input PDF
            output_path: Path to output text file
            langs: List of languages or '+'-separated string (default: eng+fra+deu)
            dpi: DPI for conversion (default: 300)
            psm: Page segmentation mode (default: 3)
        """
        langs = kwargs.get("langs", "eng+fra+deu")
        if isinstance(langs, list):
            langs = "+".join(langs)

        dpi = kwargs.get("dpi", 300)
        psm = kwargs.get("psm", 3)

        tess_config = f"--psm {psm} --oem 3"

        images = convert_from_path(input_path, dpi=dpi)

        text_parts = [f"Languages: {langs}\n"]
        for i, image in enumerate(images, start=1):
            text = pytesseract.image_to_string(image, lang=langs, config=tess_config)
            text_parts.append(f"--- Page {i} ---\n{text}")

        output_path = output_path.with_suffix(".txt")
        output_path.write_text("\n\n".join(text_parts), encoding="utf-8")
