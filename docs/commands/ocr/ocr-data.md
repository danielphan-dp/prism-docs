# ocr-data

Extract detailed OCR data with bounding boxes and confidence scores.

## Synopsis

```
prism-docs ocr-data <input> [options]
```

## Options

```
-o, --output PATH      Output JSON file path
--lang LANG            OCR language (default: eng)
--dpi N                DPI for conversion (default: 300)
--psm N                Page segmentation mode (default: 3)
--min-confidence N     Minimum confidence 0-100 (default: 0)
--level LEVEL          Data level: word, line, block, page (default: word)
```

## Examples

```shell
# Extract word-level data
prism-docs ocr-data document.pdf

# Filter low-confidence words
prism-docs ocr-data document.pdf --min-confidence 60

# Get line-level data
prism-docs ocr-data document.pdf --level line

# Block-level data
prism-docs ocr-data document.pdf --level block
```

## Output Format

JSON structure:

```json
[
  {
    "page": 1,
    "width": 2550,
    "height": 3300,
    "items": [
      {
        "text": "Hello",
        "confidence": 95,
        "bbox": {
          "x": 100,
          "y": 200,
          "width": 150,
          "height": 30
        },
        "block_num": 1,
        "line_num": 1,
        "word_num": 1
      }
    ]
  }
]
```

## Use Cases

- Document layout analysis
- Building search indexes
- Data extraction pipelines
- Quality assessment (confidence scores)
- Custom text positioning

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR installed on system

## See Also

- [ocr](ocr.md) - Basic text extraction
- [ocr-table](ocr-table.md) - Table extraction
