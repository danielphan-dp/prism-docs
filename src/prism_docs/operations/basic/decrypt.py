"""Decrypt PDF operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("decrypt")
class DecryptOperation(BasePDFOperation):
    """Decrypt a password-protected PDF file."""

    @property
    def name(self) -> str:
        return "decrypt"

    @property
    def description(self) -> str:
        return "Decrypt a password-protected PDF file"

    @property
    def default_suffix(self) -> str:
        return "decrypted"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        password: str = kwargs["password"]

        reader = PdfReader(input_path)
        writer = PdfWriter()

        if reader.is_encrypted:
            reader.decrypt(password)

        for page in reader.pages:
            writer.add_page(page)

        # Copy metadata if exists
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        with open(output_path, "wb") as f:
            writer.write(f)
