"""OCR operations for PDF text recognition."""

from prism_docs.operations.ocr.ocr_pdf import OCRPDFOperation
from prism_docs.operations.ocr.searchable_pdf import SearchablePDFOperation
from prism_docs.operations.ocr.extract_ocr_text import ExtractOCRTextOperation
from prism_docs.operations.ocr.batch_ocr import BatchOCROperation
from prism_docs.operations.ocr.ocr_data import OCRDataOperation
from prism_docs.operations.ocr.ocr_language import (
    OCRDetectLanguageOperation,
    OCRMultiLanguageOperation,
)
from prism_docs.operations.ocr.ocr_table import OCRTableOperation

# Advanced table extraction (optional - requires img2table)
try:
    from prism_docs.operations.ocr.ocr_table_v2 import OCRTableV2Operation

    _tables_available = True
except ImportError:
    _tables_available = False

__all__ = [
    "OCRPDFOperation",
    "SearchablePDFOperation",
    "ExtractOCRTextOperation",
    "BatchOCROperation",
    "OCRDataOperation",
    "OCRDetectLanguageOperation",
    "OCRMultiLanguageOperation",
    "OCRTableOperation",
    "OCRTableV2Operation",
]
