"""Split PDF operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("split")
class SplitOperation(BasePDFOperation):
    """Split a PDF into multiple files."""

    @property
    def name(self) -> str:
        return "split"

    @property
    def description(self) -> str:
        return "Split a PDF into multiple files (one per page or by ranges)"

    @property
    def default_suffix(self) -> str:
        return "split"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override to handle multiple output files."""
        input_path = Path(input_path)

        try:
            mode: str = kwargs.get("mode", "pages")  # "pages" or "ranges"
            ranges: list[tuple[int, int]] = kwargs.get("ranges", [])

            reader = PdfReader(input_path)
            output_dir = output_config.output_dir or input_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)

            output_paths = []

            if mode == "pages":
                # Split into individual pages
                for i, page in enumerate(reader.pages, start=1):
                    writer = PdfWriter()
                    writer.add_page(page)

                    output_path = output_dir / f"{input_path.stem}_page_{i}.pdf"
                    with open(output_path, "wb") as f:
                        writer.write(f)
                    output_paths.append(output_path)

            elif mode == "ranges":
                # Split by specified ranges
                for j, (start, end) in enumerate(ranges, start=1):
                    writer = PdfWriter()
                    for i in range(start - 1, min(end, len(reader.pages))):
                        writer.add_page(reader.pages[i])

                    output_path = output_dir / f"{input_path.stem}_part_{j}.pdf"
                    with open(output_path, "wb") as f:
                        writer.write(f)
                    output_paths.append(output_path)

            return OperationResult(
                success=True,
                input_path=input_path,
                output_path=output_paths[0] if output_paths else None,
                message=f"Split '{input_path}' into {len(output_paths)} files",
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to split '{input_path}': {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used for split - see execute override."""
        pass
