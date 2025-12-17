"""Interleave pages from two PDFs."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("interleave")
class InterleaveOperation(BasePDFOperation):
    """Interleave pages from two PDFs (useful for duplex scanning)."""

    @property
    def name(self) -> str:
        return "interleave"

    @property
    def description(self) -> str:
        return "Interleave pages from two PDFs (e.g., front/back from duplex scan)"

    @property
    def default_suffix(self) -> str:
        return "interleaved"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override to handle two input files."""
        input_path = Path(input_path)
        second_path: Path | None = kwargs.pop("second_path", None)

        if second_path is None:
            return OperationResult(
                success=False,
                input_path=input_path,
                message="Interleave requires a second PDF file (--second)",
            )

        second_path = Path(second_path)

        try:
            output_path = kwargs.pop("output_path", None)
            if output_path is None:
                output_path = output_config.resolve_output_path(input_path, self.default_suffix)
            else:
                output_path = Path(output_path)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            self._execute_interleave(input_path, second_path, output_path, **kwargs)

            return OperationResult(
                success=True,
                input_path=input_path,
                output_path=output_path,
                message=f"Interleaved '{input_path}' and '{second_path}' into '{output_path}'",
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to interleave: {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see _execute_interleave."""
        pass

    def _execute_interleave(
        self,
        first_path: Path,
        second_path: Path,
        output_path: Path,
        **kwargs: Any,
    ) -> None:
        reverse_second: bool = kwargs.get("reverse_second", True)
        pattern: str = kwargs.get("pattern", "alternate")  # alternate, front-back

        reader1 = PdfReader(first_path)
        reader2 = PdfReader(second_path)
        writer = PdfWriter()

        pages1 = list(reader1.pages)
        pages2 = list(reader2.pages)

        if reverse_second:
            pages2 = list(reversed(pages2))

        if pattern == "alternate":
            # Interleave: 1a, 1b, 2a, 2b, ...
            max_len = max(len(pages1), len(pages2))
            for i in range(max_len):
                if i < len(pages1):
                    writer.add_page(pages1[i])
                if i < len(pages2):
                    writer.add_page(pages2[i])

        elif pattern == "front-back":
            # All of first, then all of second
            for page in pages1:
                writer.add_page(page)
            for page in pages2:
                writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
