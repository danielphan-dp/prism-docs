"""Extract text from PDF using OCR with advanced options."""

from pathlib import Path
from typing import Any

import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("ocr-extract")
class ExtractOCRTextOperation(BasePDFOperation):
    """Extract text from PDF using OCR with preprocessing."""

    @property
    def name(self) -> str:
        return "ocr-extract"

    @property
    def description(self) -> str:
        return "Extract text from PDF using OCR with image preprocessing"

    @property
    def default_suffix(self) -> str:
        return "extracted"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        Extract text with advanced preprocessing.

        Args:
            input_path: Path to input PDF
            output_path: Path to output text file
            lang: OCR language(s) (default: eng)
            dpi: DPI for conversion (default: 300)
            psm: Page segmentation mode (default: 3)
            oem: OCR engine mode (default: 3)
            preprocess: Preprocessing mode: none, threshold, blur, sharpen, denoise (default: none)
            threshold: Binarization threshold 0-255 (default: 128)
            contrast: Contrast enhancement factor (default: 1.0)
            brightness: Brightness enhancement factor (default: 1.0)
            invert: Invert colors (default: False)
            format: Output format: text, hocr, tsv, box, data (default: text)
            timeout: Timeout per page (default: 30)
        """
        lang = kwargs.get("lang", "eng")
        dpi = kwargs.get("dpi", 300)
        psm = kwargs.get("psm", 3)
        oem = kwargs.get("oem", 3)
        preprocess = kwargs.get("preprocess", "none")
        threshold_val = kwargs.get("threshold", 128)
        contrast = kwargs.get("contrast", 1.0)
        brightness = kwargs.get("brightness", 1.0)
        invert = kwargs.get("invert", False)
        output_format = kwargs.get("format", "text")
        timeout = kwargs.get("timeout", 30)

        tess_config = f"--psm {psm} --oem {oem}"

        # Convert PDF to images
        images = convert_from_path(input_path, dpi=dpi)

        # Process each page
        results: list[str] = []
        for i, image in enumerate(images, start=1):
            # Preprocess image
            processed = self._preprocess_image(
                image,
                preprocess=preprocess,
                threshold=threshold_val,
                contrast=contrast,
                brightness=brightness,
                invert=invert,
            )

            # OCR based on output format
            if output_format == "text":
                text = pytesseract.image_to_string(
                    processed, lang=lang, config=tess_config, timeout=timeout
                )
            elif output_format == "hocr":
                hocr_result = pytesseract.image_to_pdf_or_hocr(
                    processed,
                    lang=lang,
                    config=tess_config,
                    timeout=timeout,
                    extension="hocr",
                )
                text = (
                    hocr_result.decode("utf-8") if isinstance(hocr_result, bytes) else hocr_result
                )
            elif output_format == "tsv":
                text = pytesseract.image_to_data(
                    processed, lang=lang, config=tess_config, timeout=timeout
                )
            elif output_format == "box":
                text = pytesseract.image_to_boxes(
                    processed, lang=lang, config=tess_config, timeout=timeout
                )
            elif output_format == "data":
                data = pytesseract.image_to_data(
                    processed,
                    lang=lang,
                    config=tess_config,
                    timeout=timeout,
                    output_type=pytesseract.Output.DICT,
                )
                text = str(data)
            else:
                text = pytesseract.image_to_string(
                    processed, lang=lang, config=tess_config, timeout=timeout
                )

            results.append(f"--- Page {i} ---\n{text}")

        # Determine output extension
        ext_map = {
            "text": ".txt",
            "hocr": ".hocr",
            "tsv": ".tsv",
            "box": ".box",
            "data": ".json",
        }
        output_ext = ext_map.get(output_format, ".txt")
        output_path = output_path.with_suffix(output_ext)

        # Write output
        output_path.write_text("\n\n".join(results), encoding="utf-8")

    def _preprocess_image(
        self,
        image: Image.Image,
        preprocess: str,
        threshold: int,
        contrast: float,
        brightness: float,
        invert: bool,
    ) -> Image.Image:
        """Apply preprocessing to image for better OCR."""
        # Convert to grayscale
        if image.mode != "L":
            image = image.convert("L")

        # Apply contrast
        if contrast != 1.0:
            contrast_enhancer = ImageEnhance.Contrast(image)
            image = contrast_enhancer.enhance(contrast)

        # Apply brightness
        if brightness != 1.0:
            brightness_enhancer = ImageEnhance.Brightness(image)
            image = brightness_enhancer.enhance(brightness)

        # Apply preprocessing
        if preprocess == "threshold":
            thresh = threshold  # Capture for lambda
            image = image.point(lambda p, t=thresh: 255 if p > t else 0)  # type: ignore[misc]
        elif preprocess == "blur":
            image = image.filter(ImageFilter.GaussianBlur(radius=1))
        elif preprocess == "sharpen":
            image = image.filter(ImageFilter.SHARPEN)
        elif preprocess == "denoise":
            image = image.filter(ImageFilter.MedianFilter(size=3))

        # Invert if requested
        if invert:
            from PIL import ImageOps

            image = ImageOps.invert(image)

        return image
