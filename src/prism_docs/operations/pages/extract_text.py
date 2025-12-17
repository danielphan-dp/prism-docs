"""Extract text from PDF operation."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("extract-text")
class ExtractTextOperation(BasePDFOperation):
    """Extract text from a PDF file."""

    @property
    def name(self) -> str:
        return "extract-text"

    @property
    def description(self) -> str:
        return "Extract text from a PDF file and save to a text file"

    @property
    def default_suffix(self) -> str:
        return "extracted"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override to handle .txt extension."""
        input_path = Path(input_path)

        try:
            # Build output path with .txt extension
            output_path = kwargs.pop("output_path", None)
            if output_path is None:
                stem = input_path.stem
                suffix = output_config.suffix or f"-{self.default_suffix}"
                output_dir = output_config.output_dir or input_path.parent
                output_path = output_dir / f"{stem}{suffix}.txt"
            else:
                output_path = Path(output_path)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            self._execute(input_path, output_path, **kwargs)

            return OperationResult(
                success=True,
                input_path=input_path,
                output_path=output_path,
                message=f"Extracted text from '{input_path}' to '{output_path}'",
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to extract text from '{input_path}': {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        separator: str = kwargs.get("separator", "\n\n")
        pages: list[int] | None = kwargs.get("pages")

        reader = PdfReader(input_path)

        def _page_text(page_index: int) -> str:
            text = reader.pages[page_index].extract_text()
            return text or ""

        if pages is not None:
            texts = [_page_text(p - 1) for p in pages if 1 <= p <= len(reader.pages)]
        else:
            texts = [text or "" for text in (page.extract_text() for page in reader.pages)]

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(separator.join(texts))
