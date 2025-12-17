"""Extract embedded images from PDF."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("extract-images")
class ExtractImagesOperation(BasePDFOperation):
    """Extract embedded images from a PDF."""

    @property
    def name(self) -> str:
        return "extract-images"

    @property
    def description(self) -> str:
        return "Extract embedded images from a PDF file"

    @property
    def default_suffix(self) -> str:
        return "image"

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

            count = self._extract_images(input_path, output_dir, **kwargs)

            return OperationResult(
                success=True,
                input_path=input_path,
                output_path=output_dir,
                message=f"Extracted {count} images from '{input_path}' to '{output_dir}'",
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to extract images: {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see _extract_images."""
        pass

    def _extract_images(
        self,
        input_path: Path,
        output_dir: Path,
        **kwargs: Any,
    ) -> int:
        pages: list[int] | None = kwargs.get("pages")
        min_size: int = kwargs.get("min_size", 100)  # Minimum dimension in pixels
        requested_format: str = str(kwargs.get("format", "original")).lower()

        reader = PdfReader(input_path)
        stem = input_path.stem
        image_count = 0

        for page_num, page in enumerate(reader.pages, start=1):
            # Skip pages not in the requested list
            if pages and page_num not in pages:
                continue

            resources = page.get("/Resources")
            if not resources or "/XObject" not in resources:
                continue

            x_object_ref = resources.get("/XObject")
            if not x_object_ref:
                continue
            x_objects = x_object_ref.get_object()

            for obj_name in x_objects:
                obj = x_objects[obj_name]

                if obj["/Subtype"] == "/Image":
                    try:
                        # Get image data
                        width = obj["/Width"]
                        height = obj["/Height"]

                        # Skip small images
                        if width < min_size or height < min_size:
                            continue

                        image_count += 1
                        base = output_dir / f"{stem}_p{page_num}_img{image_count}"

                        filter_type = obj.get("/Filter")
                        if isinstance(filter_type, list) and filter_type:
                            filter_type = filter_type[0]

                        if filter_type == "/DCTDecode":
                            original_ext = "jpg"
                        elif filter_type == "/JPXDecode":
                            original_ext = "jp2"
                        else:
                            original_ext = "bin"

                        if requested_format == "original" and filter_type != "/FlateDecode":
                            output_path = base.with_suffix(f".{original_ext}")
                            with open(output_path, "wb") as f:
                                f.write(obj.get_data())
                            continue

                        from io import BytesIO

                        from PIL import Image

                        img = None
                        if filter_type == "/FlateDecode":
                            data = obj.get_data()
                            color_space = obj.get("/ColorSpace")
                            bits = int(obj.get("/BitsPerComponent", 8))

                            mode = None
                            if color_space == "/DeviceRGB":
                                mode = "RGB"
                            elif color_space == "/DeviceGray":
                                mode = "L" if bits == 8 else "1"
                            elif color_space == "/DeviceCMYK":
                                mode = "CMYK"

                            if mode is not None and bits in (1, 8):
                                img = Image.frombytes(mode, (int(width), int(height)), data)
                        else:
                            try:
                                with Image.open(BytesIO(obj.get_data())) as opened:
                                    img = opened.copy()
                            except Exception:
                                img = None

                        if img is None:
                            output_path = base.with_suffix(f".{original_ext}")
                            with open(output_path, "wb") as f:
                                f.write(obj.get_data())
                            continue

                        output_ext = requested_format
                        if output_ext == "jpeg":
                            output_ext = "jpg"
                        if requested_format == "original":
                            output_ext = "png"

                        if output_ext in {"jpg", "jpeg"} and img.mode not in {"RGB", "L"}:
                            img = img.convert("RGB")

                        output_path = base.with_suffix(f".{output_ext}")
                        img.save(output_path)

                    except Exception:
                        # Skip problematic images
                        continue

        return image_count
