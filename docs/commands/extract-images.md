# extract-images

Extract embedded images from PDF.

## Synopsis

```
prism-docs extract-images <input> [options]
```

## Options

```
--output-dir PATH      Output directory (default: current)
--format FMT           Output format: original, png, jpeg (default: original)
--min-size N           Minimum image dimension in pixels
```

## Examples

```shell
# Extract all images
prism-docs extract-images document.pdf

# Extract to specific directory
prism-docs extract-images document.pdf --output-dir ./images

# Keep original encoded image format when possible
prism-docs extract-images document.pdf --format original

# Force PNG/JPEG output
prism-docs extract-images document.pdf --format png
prism-docs extract-images document.pdf --format jpeg
```

## Requirements

Requires image extras: `uv sync --extra images`

## See Also

- [pdf-to-images](pdf-to-images.md) - Convert pages to images
