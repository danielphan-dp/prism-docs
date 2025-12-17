"""Get detailed OCR data with bounding boxes and confidence."""

from pathlib import Path
from typing import Any
import json

import pytesseract
from pdf2image import convert_from_path

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("ocr-data")
class OCRDataOperation(BasePDFOperation):
    """Extract detailed OCR data with positions and confidence scores."""

    @property
    def name(self) -> str:
        return "ocr-data"

    @property
    def description(self) -> str:
        return "Extract OCR data with bounding boxes and confidence scores"

    @property
    def default_suffix(self) -> str:
        return "ocr-data"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        Extract detailed OCR data.

        Args:
            input_path: Path to input PDF
            output_path: Path to output JSON file
            lang: OCR language(s) (default: eng)
            dpi: DPI for conversion (default: 300)
            psm: Page segmentation mode (default: 3)
            min_confidence: Minimum confidence threshold 0-100 (default: 0)
            level: Data level: word, line, block, page (default: word)
        """
        lang = kwargs.get("lang", "eng")
        dpi = kwargs.get("dpi", 300)
        psm = kwargs.get("psm", 3)
        min_confidence = kwargs.get("min_confidence", 0)
        level = kwargs.get("level", "word")

        tess_config = f"--psm {psm} --oem 3"

        images = convert_from_path(input_path, dpi=dpi)

        # Level mapping for Tesseract
        level_map = {"page": 1, "block": 2, "para": 3, "line": 4, "word": 5}
        target_level = level_map.get(level, 5)

        all_pages_data = []
        for page_num, image in enumerate(images, start=1):
            # Get detailed data
            data = pytesseract.image_to_data(
                image,
                lang=lang,
                config=tess_config,
                output_type=pytesseract.Output.DICT,
            )

            # Process data
            page_items = []
            n_boxes = len(data["text"])

            for i in range(n_boxes):
                # Filter by level
                if data["level"][i] != target_level:
                    continue

                # Filter by confidence
                conf = data["conf"][i]
                if conf < min_confidence:
                    continue

                text = data["text"][i].strip()
                if not text:
                    continue

                item = {
                    "text": text,
                    "confidence": conf,
                    "bbox": {
                        "x": data["left"][i],
                        "y": data["top"][i],
                        "width": data["width"][i],
                        "height": data["height"][i],
                    },
                    "block_num": data["block_num"][i],
                    "line_num": data["line_num"][i],
                    "word_num": data["word_num"][i],
                }
                page_items.append(item)

            all_pages_data.append(
                {
                    "page": page_num,
                    "width": image.width,
                    "height": image.height,
                    "items": page_items,
                }
            )

        # Write JSON output
        output_path = output_path.with_suffix(".json")
        output_path.write_text(
            json.dumps(all_pages_data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
