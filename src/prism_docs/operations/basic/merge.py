"""Merge PDFs operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("merge")
class MergeOperation(BasePDFOperation):
    """Merge multiple PDF files into one."""

    @property
    def name(self) -> str:
        return "merge"

    @property
    def description(self) -> str:
        return "Merge multiple PDF files into one"

    @property
    def default_suffix(self) -> str:
        return "merged"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override execute for merge since it handles multiple inputs differently."""
        input_paths: list[Path] = kwargs.get("merge_inputs", [input_path])
        output_path: Path | None = kwargs.pop("output_path", None)

        if output_path is None:
            output_path = output_config.resolve_output_path(input_paths[0], self.default_suffix)

        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            self._execute_merge(input_paths, output_path)

            return OperationResult(
                success=True,
                input_path=input_paths[0],
                output_path=output_path,
                message=f"Merged {len(input_paths)} PDFs into '{output_path}'",
            )
        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_paths[0],
                message=f"Failed to merge PDFs: {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used for merge - see _execute_merge."""
        pass

    def _execute_merge(self, input_paths: list[Path], output_path: Path) -> None:
        """Execute the merge operation."""
        writer = PdfWriter()

        for pdf_path in input_paths:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
