"""Convert PDF pages to images."""

from pathlib import Path
from typing import Any

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("pdf-to-images")
class PdfToImagesOperation(BasePDFOperation):
    """Convert PDF pages to images."""

    @property
    def name(self) -> str:
        return "pdf-to-images"

    @property
    def description(self) -> str:
        return "Convert PDF pages to images (PNG, JPG)"

    @property
    def default_suffix(self) -> str:
        return "page"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override to handle multiple output files."""
        input_path = Path(input_path)

        try:
            output_dir = kwargs.get("output_dir") or output_config.output_dir or input_path.parent
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            output_paths = self._execute_pdf_to_images(input_path, output_dir, **kwargs)

            return OperationResult(
                success=True,
                input_path=input_path,
                output_path=output_paths[0] if output_paths else None,
                message=f"Converted '{input_path}' to {len(output_paths)} images",
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to convert PDF to images: {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see _execute_pdf_to_images."""
        pass

    def _execute_pdf_to_images(
        self,
        input_path: Path,
        output_dir: Path,
        **kwargs: Any,
    ) -> list[Path]:
        try:
            import pdf2image
        except ImportError:
            raise ImportError(
                "pdf2image is required for PDF to image conversion. "
                "Install with: pip install pdf2image"
            )

        format: str = kwargs.get("format", "png")
        dpi: int = kwargs.get("dpi", 200)
        pages: list[int] | None = kwargs.get("pages")

        # Convert pages (1-indexed) to pdf2image format
        if pages:
            first_page = min(pages)
            last_page = max(pages)
            images = pdf2image.convert_from_path(
                input_path,
                dpi=dpi,
                first_page=first_page,
                last_page=last_page,
                fmt=format,
            )
        else:
            first_page = None
            images = pdf2image.convert_from_path(
                input_path,
                dpi=dpi,
                fmt=format,
            )

        output_paths = []
        stem = input_path.stem

        for i, image in enumerate(images):
            page_num = (first_page or 1) + i
            # Skip pages not in the requested list
            if pages and page_num not in pages:
                continue

            output_path = output_dir / f"{stem}_page_{page_num}.{format}"
            image.save(output_path)
            output_paths.append(output_path)

        return output_paths
