"""Prism Docs - CLI toolkit for PDF editing, security, OCR, and image conversion."""

# Import operations to register them
import prism_docs.operations  # noqa: F401
from prism_docs.core import (
    BasePDFOperation,
    Config,
    GlobalConfig,
    OperationConfig,
    OperationResult,
    OutputConfig,
    OutputNaming,
    OverwritePolicy,
    load_config,
    register_operation,
    registry,
)
from prism_docs.core.runner import PDFRunner, run_operation

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Core types
    "BasePDFOperation",
    "OperationResult",
    "OutputConfig",
    "OutputNaming",
    "OverwritePolicy",
    "OperationConfig",
    # Config
    "Config",
    "GlobalConfig",
    "load_config",
    # Registry
    "registry",
    "register_operation",
    # Runner
    "PDFRunner",
    "run_operation",
]
