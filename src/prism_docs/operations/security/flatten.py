"""Flatten PDF annotations and forms."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject

from prism_docs.core import BasePDFOperation, register_operation


@register_operation("flatten")
class FlattenOperation(BasePDFOperation):
    """Flatten PDF annotations and form fields."""

    @property
    def name(self) -> str:
        return "flatten"

    @property
    def description(self) -> str:
        return "Flatten annotations and form fields into page content"

    @property
    def default_suffix(self) -> str:
        return "flattened"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        flatten_forms: bool = kwargs.get("forms", True)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Flatten form fields if present
        root = reader.trailer.get("/Root")
        if flatten_forms and root and "/AcroForm" in root:
            # Reset form fields to make them non-editable
            for page_num in range(len(writer.pages)):
                page = writer.pages[page_num]
                if "/Annots" in page:
                    annotations = page["/Annots"]
                    if annotations:
                        annot_array = (
                            annotations.get_object()
                            if hasattr(annotations, "get_object")
                            else annotations
                        )
                        if hasattr(annot_array, "__iter__"):
                            for annot in annot_array:  # type: ignore[union-attr]
                                annot_obj = (
                                    annot.get_object() if hasattr(annot, "get_object") else annot
                                )
                                if (
                                    hasattr(annot_obj, "get")
                                    and annot_obj.get("/Subtype") == "/Widget"
                                ):
                                    # Set read-only flag; keep existing bits if present
                                    current_flags = annot_obj.get("/Ff", 0)
                                    annot_obj[NameObject("/Ff")] = NumberObject(
                                        int(current_flags) | 1
                                    )  # type: ignore[index]

        with open(output_path, "wb") as f:
            writer.write(f)
