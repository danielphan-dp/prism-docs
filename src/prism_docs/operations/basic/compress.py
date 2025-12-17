"""Compress PDF operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("compress")
class CompressOperation(BasePDFOperation):
    """Compress a PDF file using lossless compression."""

    @property
    def name(self) -> str:
        return "compress"

    @property
    def description(self) -> str:
        return "Compress a PDF file using lossless compression"

    @property
    def default_suffix(self) -> str:
        return "compressed"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        compress_streams: bool = kwargs.get("compress_streams", True)

        reader = PdfReader(input_path)
        writer = PdfWriter(clone_from=reader)

        for page in writer.pages:
            if compress_streams:
                page.compress_content_streams()

        # Copy metadata
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        with open(output_path, "wb") as f:
            writer.write(f)
