# ocr

Extract text from scanned PDF using Tesseract OCR.

## Synopsis

```
prism-docs ocr <input> [options]
```

## Options

```
-o, --output PATH      Output text file path
--lang LANG            OCR language (default: eng)
--dpi N                DPI for conversion (default: 300)
--psm N                Page segmentation mode (default: 3)
--oem N                OCR engine mode (default: 3)
--config STR           Additional Tesseract config
--pages SPEC           Pages to OCR (default: all)
--timeout N            Timeout per page in seconds (default: 30)
```

## Examples

```shell
# Basic OCR
prism-docs ocr scanned.pdf

# Specify language
prism-docs ocr document.pdf --lang fra

# Multiple languages
prism-docs ocr mixed.pdf --lang eng+fra+deu

# Higher quality (slower)
prism-docs ocr document.pdf --dpi 400

# Specific pages
prism-docs ocr book.pdf --pages 1-10
```

## Output

Produces a `.txt` file with extracted text, separated by page markers.

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR installed on system

## See Also

- [ocr-extract](ocr-extract.md) - OCR with preprocessing
- [searchable-pdf](searchable-pdf.md) - Create searchable PDF
