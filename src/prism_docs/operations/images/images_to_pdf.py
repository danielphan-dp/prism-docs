"""Convert images to PDF."""

from pathlib import Path
from typing import Any

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("images-to-pdf")
class ImagesToPdfOperation(BasePDFOperation):
    """Convert images to a PDF file."""

    @property
    def name(self) -> str:
        return "images-to-pdf"

    @property
    def description(self) -> str:
        return "Convert images (PNG, JPG, etc.) to a PDF file"

    @property
    def default_suffix(self) -> str:
        return "converted"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Override to handle multiple image inputs."""
        image_paths: list[Path] = kwargs.pop("image_paths", [Path(input_path)])
        image_paths = [Path(p) for p in image_paths]

        try:
            output_path = kwargs.pop("output_path", None)
            if output_path is None:
                output_path = output_config.resolve_output_path(
                    image_paths[0].with_suffix(".pdf"), self.default_suffix
                )
            else:
                output_path = Path(output_path)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            self._execute_images_to_pdf(image_paths, output_path, **kwargs)

            return OperationResult(
                success=True,
                input_path=image_paths[0],
                output_path=output_path,
                message=f"Converted {len(image_paths)} images to '{output_path}'",
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=image_paths[0] if image_paths else Path("."),
                message=f"Failed to convert images: {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see _execute_images_to_pdf."""
        pass

    def _execute_images_to_pdf(
        self,
        image_paths: list[Path],
        output_path: Path,
        **kwargs: Any,
    ) -> None:
        from PIL import Image

        images: list[Any] = []
        for img_path in image_paths:
            img = Image.open(img_path)
            if img.mode == "RGBA":
                # Convert RGBA to RGB with white background
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)

        if not images:
            raise ValueError("No images provided")

        # Save as PDF
        first_image = images[0]
        if len(images) > 1:
            first_image.save(
                output_path,
                "PDF",
                save_all=True,
                append_images=images[1:],
            )
        else:
            first_image.save(output_path, "PDF")
