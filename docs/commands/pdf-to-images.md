# pdf-to-images

Convert PDF pages to images.

## Synopsis

```
prism-docs pdf-to-images <input> [options]
```

## Options

```
--output-dir PATH      Output directory (default: current)
--format FMT           Image format: png, jpg, tiff (default: png)
--dpi N                Resolution in DPI (default: 150)
--pages SPEC           Pages to convert (default: all)
```

## Examples

```shell
# Convert all pages to PNG
prism-docs pdf-to-images document.pdf

# Convert to JPEG at higher DPI
prism-docs pdf-to-images document.pdf --format jpg --dpi 300

# Convert specific pages
prism-docs pdf-to-images document.pdf --pages 1-5 --output-dir ./images
```

## Requirements

Requires image extras: `uv sync --extra images`

## See Also

- [images-to-pdf](images-to-pdf.md) - Convert images to PDF
- [extract-images](extract-images.md) - Extract embedded images
