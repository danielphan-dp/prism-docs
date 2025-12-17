"""Encrypt PDF operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("encrypt")
class EncryptOperation(BasePDFOperation):
    """Encrypt a PDF file with a password."""

    @property
    def name(self) -> str:
        return "encrypt"

    @property
    def description(self) -> str:
        return "Encrypt a PDF file with a password"

    @property
    def default_suffix(self) -> str:
        return "encrypted"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        password: str = kwargs["password"]
        owner_password: str | None = kwargs.get("owner_password")
        algorithm: str = kwargs.get("algorithm", "AES-256")

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Copy metadata if exists
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        writer.encrypt(
            user_password=password,
            owner_password=owner_password or password,
            algorithm=algorithm,
        )

        with open(output_path, "wb") as f:
            writer.write(f)
