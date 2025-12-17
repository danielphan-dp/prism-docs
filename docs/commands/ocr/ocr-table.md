# ocr-table

Extract tables from scanned PDFs using OCR.

## Synopsis

```
prism-docs ocr-table <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--lang LANG            OCR language (default: eng)
--dpi N                DPI for conversion (default: 300)
--format FMT           Output format: csv, tsv, json (default: csv)
--pages SPEC           Pages to extract (default: all)
```

## Examples

```shell
# Extract tables to CSV
prism-docs ocr-table document.pdf

# TSV output
prism-docs ocr-table document.pdf --format tsv

# JSON for programmatic use
prism-docs ocr-table document.pdf --format json

# Specific pages
prism-docs ocr-table report.pdf --pages 5-10 -o tables.csv
```

## Output Formats

### CSV/TSV

```csv
# Page 1
Name,Age,City
John,30,NYC
Jane,25,LA

# Page 2
...
```

### JSON

```json
[
  {
    "page": 1,
    "rows": [
      ["Name", "Age", "City"],
      ["John", "30", "NYC"],
      ["Jane", "25", "LA"]
    ]
  }
]
```

## Notes

- Uses PSM 3 (auto page segmentation) for mixed content
- Works best with clean, well-structured tables
- May need manual cleanup for complex layouts
- Consider preprocessing for poor quality scans

## Tips

- Use `--dpi 400` for small text
- Clean scans work best
- Simple grid tables work better than complex layouts

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR installed on system

## See Also

- [ocr-data](ocr-data.md) - Detailed position data
- [ocr-extract](ocr-extract.md) - OCR with preprocessing
