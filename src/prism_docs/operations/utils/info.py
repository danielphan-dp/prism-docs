"""Show PDF information."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("info")
class InfoOperation(BasePDFOperation):
    """Show PDF information and metadata."""

    @property
    def name(self) -> str:
        return "info"

    @property
    def description(self) -> str:
        return "Show PDF information (pages, size, metadata, encryption)"

    @property
    def default_suffix(self) -> str:
        return ""

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override to return info without creating output file."""
        input_path = Path(input_path)

        try:
            info = self._get_info(input_path, **kwargs)

            return OperationResult(
                success=True,
                input_path=input_path,
                message=info,
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to read PDF info: {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see execute override."""
        pass

    def _get_info(self, input_path: Path, **kwargs: Any) -> str:
        verbose: bool = kwargs.get("verbose", False)
        json_output: bool = kwargs.get("json", False)

        reader = PdfReader(input_path)

        # Basic info
        info = {
            "file": str(input_path),
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
        }

        # File size
        file_size = input_path.stat().st_size
        if file_size < 1024:
            info["size"] = f"{file_size} B"
        elif file_size < 1024 * 1024:
            info["size"] = f"{file_size / 1024:.1f} KB"
        else:
            info["size"] = f"{file_size / (1024 * 1024):.1f} MB"

        # Page dimensions (from first page)
        if reader.pages:
            page = reader.pages[0]
            media_box = page.mediabox
            width_pt = float(media_box.width)
            height_pt = float(media_box.height)
            # Convert to inches
            width_in = width_pt / 72
            height_in = height_pt / 72
            info["page_size"] = (
                f"{width_pt:.0f} x {height_pt:.0f} pt ({width_in:.1f} x {height_in:.1f} in)"
            )

        # Metadata
        if reader.metadata:
            meta = reader.metadata
            info["title"] = meta.title
            info["author"] = meta.author
            info["subject"] = meta.subject
            info["creator"] = meta.creator
            info["producer"] = meta.producer
            if meta.creation_date:
                info["created"] = str(meta.creation_date)
            if meta.modification_date:
                info["modified"] = str(meta.modification_date)

        # PDF version
        if hasattr(reader, "pdf_header"):
            info["version"] = reader.pdf_header

        if json_output:
            import json

            return json.dumps(info, indent=2, default=str)

        # Format as text
        lines = [f"PDF Info: {input_path.name}"]
        lines.append("-" * 40)
        lines.append(f"  Pages: {info['pages']}")
        lines.append(f"  Size: {info['size']}")
        if "page_size" in info:
            lines.append(f"  Page Size: {info['page_size']}")
        lines.append(f"  Encrypted: {info['encrypted']}")

        if verbose and reader.metadata:
            lines.append("")
            lines.append("Metadata:")
            for key in ["title", "author", "subject", "creator", "producer", "created", "modified"]:
                if key in info and info[key]:
                    lines.append(f"  {key.title()}: {info[key]}")

        return "\n".join(lines)
