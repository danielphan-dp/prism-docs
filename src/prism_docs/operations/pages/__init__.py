"""Page manipulation operations (extract, rotate, split, remove, etc.)."""

from prism_docs.operations.pages.extract_pages import ExtractPagesOperation
from prism_docs.operations.pages.extract_text import ExtractTextOperation
from prism_docs.operations.pages.interleave import InterleaveOperation
from prism_docs.operations.pages.overlay import OverlayOperation
from prism_docs.operations.pages.page_numbers import PageNumbersOperation
from prism_docs.operations.pages.remove_pages import RemovePagesOperation
from prism_docs.operations.pages.reverse import ReverseOperation
from prism_docs.operations.pages.rotate import RotateOperation
from prism_docs.operations.pages.split import SplitOperation
from prism_docs.operations.pages.stamp import StampOperation

__all__ = [
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
]
