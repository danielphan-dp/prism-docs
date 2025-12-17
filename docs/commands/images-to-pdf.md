# images-to-pdf

Convert images to PDF.

## Synopsis

```
prism-docs images-to-pdf <image>... [options]
```

## Options

```
-o, --output PATH      Output file path (required)
--page-size SIZE       Page size: A4, Letter, etc. (default: A4)
--margin N             Page margin in points (default: 0)
```

## Examples

```shell
# Convert images to PDF
prism-docs images-to-pdf photo1.jpg photo2.jpg -o album.pdf

# Using glob
prism-docs images-to-pdf *.jpg -o photos.pdf

# Custom page size
prism-docs images-to-pdf scan*.png -o document.pdf --page-size Letter
```

## Requirements

Requires image extras: `uv sync --extra images`

## See Also

- [pdf-to-images](pdf-to-images.md) - Convert PDF to images
