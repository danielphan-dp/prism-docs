# searchable-pdf

Create a searchable PDF by adding an invisible OCR text layer.

## Synopsis

```
prism-docs searchable-pdf <input> [options]
```

## Options

```
-o, --output PATH      Output PDF path
--lang LANG            OCR language (default: eng)
--dpi N                DPI for conversion (default: 300)
--psm N                Page segmentation mode (default: 3)
--oem N                OCR engine mode (default: 3)
--timeout N            Timeout per page in seconds (default: 60)
```

## Examples

```shell
# Create searchable PDF
prism-docs searchable-pdf scanned.pdf

# With language
prism-docs searchable-pdf document.pdf --lang deu -o searchable.pdf

# Higher quality
prism-docs searchable-pdf document.pdf --dpi 400
```

## Output

Produces a PDF file with an invisible text layer that enables:

- Text search (Ctrl+F)
- Text selection and copying
- Indexing by search engines

## Notes

- Original images are preserved
- Text layer is invisible but selectable
- File size may increase slightly

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR installed on system

## See Also

- [ocr](ocr.md) - Extract text only
- [ocr-extract](ocr-extract.md) - OCR with preprocessing
