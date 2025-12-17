"""Basic PDF operations (encrypt, decrypt, merge, compress, etc.)."""

from prism_docs.operations.basic.compress import CompressOperation
from prism_docs.operations.basic.decrypt import DecryptOperation
from prism_docs.operations.basic.encrypt import EncryptOperation
from prism_docs.operations.basic.merge import MergeOperation
from prism_docs.operations.basic.metadata import MetadataOperation
from prism_docs.operations.basic.watermark import WatermarkOperation

__all__ = [
    "CompressOperation",
    "DecryptOperation",
    "EncryptOperation",
    "MergeOperation",
    "MetadataOperation",
    "WatermarkOperation",
]
