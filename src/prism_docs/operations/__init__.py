"""PDF operations module."""

# Import all operations to register them
# Basic operations
from prism_docs.operations.basic import (
    CompressOperation,
    DecryptOperation,
    EncryptOperation,
    MergeOperation,
    MetadataOperation,
    WatermarkOperation,
)

# Page manipulation operations
from prism_docs.operations.pages import (
    ExtractPagesOperation,
    ExtractTextOperation,
    InterleaveOperation,
    OverlayOperation,
    PageNumbersOperation,
    RemovePagesOperation,
    ReverseOperation,
    RotateOperation,
    SplitOperation,
    StampOperation,
)

# Image operations
from prism_docs.operations.images import (
    ExtractImagesOperation,
    ImagesToPdfOperation,
    PdfToImagesOperation,
)

# Security operations
from prism_docs.operations.security import (
    FlattenOperation,
    PermissionsOperation,
    RedactOperation,
)

# Utility operations
from prism_docs.operations.utils import (
    BookmarksOperation,
    CropOperation,
    InfoOperation,
    ResizeOperation,
    ValidateOperation,
)

# OCR operations (optional - requires pytesseract)
try:
    from prism_docs.operations.ocr import (
        OCRPDFOperation,
        SearchablePDFOperation,
        ExtractOCRTextOperation,
        BatchOCROperation,
        OCRDataOperation,
        OCRDetectLanguageOperation,
        OCRMultiLanguageOperation,
        OCRTableOperation,
    )

    _ocr_available = True
except ImportError:
    _ocr_available = False

# Advanced table extraction (optional - requires img2table)
try:
    from prism_docs.operations.ocr import OCRTableV2Operation

    _tables_v2_available = True
except ImportError:
    _tables_v2_available = False

__all__ = [
    # Basic
    "CompressOperation",
    "DecryptOperation",
    "EncryptOperation",
    "MergeOperation",
    "MetadataOperation",
    "WatermarkOperation",
    # Pages
    "ExtractPagesOperation",
    "ExtractTextOperation",
    "InterleaveOperation",
    "OverlayOperation",
    "PageNumbersOperation",
    "RemovePagesOperation",
    "ReverseOperation",
    "RotateOperation",
    "SplitOperation",
    "StampOperation",
    # Images
    "ExtractImagesOperation",
    "ImagesToPdfOperation",
    "PdfToImagesOperation",
    # Security
    "FlattenOperation",
    "PermissionsOperation",
    "RedactOperation",
    # Utils
    "BookmarksOperation",
    "CropOperation",
    "InfoOperation",
    "ResizeOperation",
    "ValidateOperation",
    # OCR (optional)
    "OCRPDFOperation",
    "SearchablePDFOperation",
    "ExtractOCRTextOperation",
    "BatchOCROperation",
    "OCRDataOperation",
    "OCRDetectLanguageOperation",
    "OCRMultiLanguageOperation",
    "OCRTableOperation",
    # Advanced tables (optional)
    "OCRTableV2Operation",
]
