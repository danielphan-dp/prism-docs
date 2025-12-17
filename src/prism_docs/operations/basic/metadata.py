"""PDF metadata operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("metadata")
class MetadataOperation(BasePDFOperation):
    """View or edit PDF metadata."""

    @property
    def name(self) -> str:
        return "metadata"

    @property
    def description(self) -> str:
        return "View or edit PDF metadata (title, author, etc.)"

    @property
    def default_suffix(self) -> str:
        return "metadata"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override for metadata viewing/editing."""
        input_path = Path(input_path)
        action: str = kwargs.get("action", "view")  # "view" or "edit"

        try:
            if action == "view":
                return self._view_metadata(input_path)
            else:
                return self._edit_metadata(input_path, output_config, **kwargs)

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to process metadata: {e}",
                error=e,
            )

    def _view_metadata(self, input_path: Path) -> OperationResult:
        """View PDF metadata."""
        reader = PdfReader(input_path)
        metadata = reader.metadata

        if metadata:
            info = {
                "Title": metadata.title,
                "Author": metadata.author,
                "Subject": metadata.subject,
                "Creator": metadata.creator,
                "Producer": metadata.producer,
                "Creation Date": str(metadata.creation_date) if metadata.creation_date else None,
                "Modification Date": str(metadata.modification_date)
                if metadata.modification_date
                else None,
            }
            message = "\n".join(f"  {k}: {v}" for k, v in info.items() if v)
        else:
            message = "No metadata found"

        return OperationResult(
            success=True,
            input_path=input_path,
            message=f"Metadata for '{input_path}':\n{message}",
        )

    def _edit_metadata(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Edit PDF metadata."""
        output_path = output_config.resolve_output_path(input_path, self.default_suffix)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Build metadata dict
        new_metadata = {}
        if "title" in kwargs:
            new_metadata["/Title"] = kwargs["title"]
        if "author" in kwargs:
            new_metadata["/Author"] = kwargs["author"]
        if "subject" in kwargs:
            new_metadata["/Subject"] = kwargs["subject"]

        if new_metadata:
            writer.add_metadata(new_metadata)

        with open(output_path, "wb") as f:
            writer.write(f)

        return OperationResult(
            success=True,
            input_path=input_path,
            output_path=output_path,
            message=f"Updated metadata and saved to '{output_path}'",
        )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see execute override."""
        pass
