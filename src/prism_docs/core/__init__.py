"""Core module exports."""

from prism_docs.core.config import Config, GlobalConfig, load_config
from prism_docs.core.registry import OperationRegistry, register_operation, registry
from prism_docs.core.types import (
    BasePDFOperation,
    OperationConfig,
    OperationResult,
    OutputConfig,
    OutputNaming,
    OverwritePolicy,
    PDFOperation,
)

__all__ = [
    # Types
    "BasePDFOperation",
    "PDFOperation",
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
    "OperationRegistry",
    "registry",
    "register_operation",
]
