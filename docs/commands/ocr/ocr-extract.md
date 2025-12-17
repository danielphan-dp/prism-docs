# ocr-extract

Extract text from PDF using OCR with image preprocessing for better results.

## Synopsis

```
prism-docs ocr-extract <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--lang LANG            OCR language (default: eng)
--dpi N                DPI for conversion (default: 300)
--psm N                Page segmentation mode (default: 3)
--oem N                OCR engine mode (default: 3)
--preprocess MODE      Preprocessing: none, threshold, blur, sharpen, denoise
--threshold N          Binarization threshold 0-255 (default: 128)
--contrast FLOAT       Contrast factor (default: 1.0)
--brightness FLOAT     Brightness factor (default: 1.0)
--invert               Invert colors
--format FMT           Output: text, hocr, tsv, box, data (default: text)
--timeout N            Timeout per page (default: 30)
```

## Examples

```shell
# Basic extraction
prism-docs ocr-extract document.pdf

# With preprocessing for poor scans
prism-docs ocr-extract faded.pdf --preprocess threshold --threshold 150

# Sharpen blurry scans
prism-docs ocr-extract blurry.pdf --preprocess sharpen --contrast 1.5

# Denoise grainy scans
prism-docs ocr-extract grainy.pdf --preprocess denoise

# Invert dark background
prism-docs ocr-extract dark.pdf --invert

# Get hOCR output (with positions)
prism-docs ocr-extract document.pdf --format hocr
```

## Preprocessing Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `none` | No preprocessing | Clean scans |
| `threshold` | Binary threshold | Faded text, low contrast |
| `blur` | Gaussian blur | Noise reduction |
| `sharpen` | Sharpen filter | Blurry scans |
| `denoise` | Median filter | Grainy/speckled images |

## Output Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| `text` | `.txt` | Plain text |
| `hocr` | `.hocr` | HTML with bounding boxes |
| `tsv` | `.tsv` | Tab-separated data |
| `box` | `.box` | Character bounding boxes |
| `data` | `.json` | Full OCR data dict |

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR installed on system

## See Also

- [ocr](ocr.md) - Basic OCR
- [ocr-data](ocr-data.md) - Detailed OCR data
