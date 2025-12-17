# ocr-batch

Batch OCR multiple PDFs with consistent settings.

## Synopsis

```
prism-docs ocr-batch <input>... [options]
```

## Options

```
--lang LANG            OCR language (default: eng)
--dpi N                DPI for conversion (default: 300)
--psm N                Page segmentation mode (default: 3)
--output-type TYPE     Output type: txt, pdf (default: txt)
--fast                 Fast mode with lower DPI
--output-dir PATH      Output directory
```

## Examples

```shell
# Batch OCR to text files
prism-docs ocr-batch *.pdf

# Create searchable PDFs
prism-docs ocr-batch scans/*.pdf --output-type pdf

# Fast mode for quick processing
prism-docs ocr-batch documents/*.pdf --fast

# Specify output directory
prism-docs ocr-batch *.pdf --output-dir ./ocr-output

# With parallel processing
prism-docs --parallel ocr-batch *.pdf
```

## Output

- `txt`: One `.txt` file per input PDF
- `pdf`: One searchable PDF per input

## Notes

- Use `--fast` for drafts (lower quality, faster)
- Use `--parallel` flag for multi-core processing
- Consistent settings across all files

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR installed on system

## See Also

- [ocr](ocr.md) - Single file OCR
- [searchable-pdf](searchable-pdf.md) - Create searchable PDF
