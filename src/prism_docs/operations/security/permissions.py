"""Set PDF permissions."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("permissions")
class PermissionsOperation(BasePDFOperation):
    """Set PDF permissions (print, copy, modify, etc.)."""

    @property
    def name(self) -> str:
        return "permissions"

    @property
    def description(self) -> str:
        return "Set PDF permissions (print, copy, modify restrictions)"

    @property
    def default_suffix(self) -> str:
        return "restricted"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        owner_password: str = kwargs.get("owner_password", "")
        user_password: str = kwargs.get("user_password", "")

        # Permission flags
        allow_print: bool = kwargs.get("print", True)
        allow_copy: bool = kwargs.get("copy", True)
        allow_modify: bool = kwargs.get("modify", False)
        allow_annotations: bool = kwargs.get("annotations", True)
        allow_forms: bool = kwargs.get("forms", True)
        allow_extract: bool = kwargs.get("extract", True)
        allow_assemble: bool = kwargs.get("assemble", False)
        print_quality: str = kwargs.get("print_quality", "high")  # high or low

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Copy metadata
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        # Build permissions
        permissions = UserAccessPermissions.all()

        if not allow_print:
            permissions &= ~UserAccessPermissions.PRINT
            permissions &= ~UserAccessPermissions.PRINT_TO_REPRESENTATION
        elif print_quality == "low":
            permissions &= ~UserAccessPermissions.PRINT_TO_REPRESENTATION

        if not allow_copy:
            permissions &= ~UserAccessPermissions.EXTRACT
            permissions &= ~UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS

        if not allow_modify:
            permissions &= ~UserAccessPermissions.MODIFY

        if not allow_annotations:
            permissions &= ~UserAccessPermissions.ADD_OR_MODIFY

        if not allow_forms:
            permissions &= ~UserAccessPermissions.FILL_FORM_FIELDS

        if not allow_extract:
            permissions &= ~UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS

        if not allow_assemble:
            # DOCUMENT_ASSEMBLY may not be available in all pypdf versions
            doc_assembly = getattr(UserAccessPermissions, "DOCUMENT_ASSEMBLY", None)
            if doc_assembly is not None:
                permissions &= ~doc_assembly

        # Encrypt with permissions
        writer.encrypt(
            user_password=user_password,
            owner_password=owner_password or user_password or "owner",
            permissions_flag=permissions,
        )

        with open(output_path, "wb") as f:
            writer.write(f)
