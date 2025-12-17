# ocr-table-v2

Extract tables from scanned PDFs using advanced detection.

## Synopsis

```
prism-docs ocr-table-v2 <input> -o <output> [options]
```

## Options

```
-o, --output PATH          Output file path (required)
--lang LANG                OCR language (default: eng)
--format {csv,tsv,json,xlsx}  Output format (default: csv)
--pages SPEC               Pages to extract (e.g., "1-5" or "1,3,5")
--implicit-rows            Detect implicit rows (default: enabled)
--no-implicit-rows         Disable implicit row detection
--borderless               Detect borderless tables (default: enabled)
--no-borderless            Only detect bordered tables
--min-confidence N         Minimum confidence (0-100) (default: 50)
```

## Examples

```shell
# Extract tables to CSV
prism-docs ocr-table-v2 scan.pdf -o tables.csv

# Extract only certain pages
prism-docs ocr-table-v2 scan.pdf -o tables.csv --pages "2-4"

# Output XLSX and tune detection
prism-docs ocr-table-v2 scan.pdf -o tables.xlsx --no-borderless --min-confidence 70
```

## See Also

- [ocr](ocr.md) - Extract text from scanned PDFs
- [ocr-table](ocr-table.md) - Table extraction (basic)
