# OCR Commands

Optical Character Recognition (OCR) operations for scanned PDFs.

**Requirements:**

```shell
uv sync --extra ocr

# System dependency: Tesseract OCR
# Ubuntu/Debian: sudo apt install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## Commands

| Command | Description |
|---------|-------------|
| [ocr](ocr.md) | Extract text from scanned PDF |
| [searchable-pdf](searchable-pdf.md) | Create searchable PDF with text layer |
| [ocr-extract](ocr-extract.md) | OCR with image preprocessing |
| [ocr-batch](ocr-batch.md) | Batch OCR multiple PDFs |
| [ocr-data](ocr-data.md) | Extract OCR data with positions |
| [ocr-detect-lang](ocr-detect-lang.md) | Auto-detect language and OCR |
| [ocr-multi-lang](ocr-multi-lang.md) | OCR mixed-language documents |
| [ocr-table](ocr-table.md) | Extract tables from scanned PDFs |
| [ocr-table-v2](ocr-table-v2.md) | Extract tables using advanced detection |

## Common Options

All OCR commands support:

```
--lang LANG            Tesseract language code (default: eng)
--dpi N                DPI for PDF to image conversion (default: 300)
--psm N                Page segmentation mode (default: 3)
--oem N                OCR engine mode (default: 3)
```

## Language Codes

```
eng     English
fra     French
deu     German
spa     Spanish
ita     Italian
por     Portuguese
rus     Russian
chi_sim Chinese (Simplified)
chi_tra Chinese (Traditional)
jpn     Japanese
kor     Korean
ara     Arabic
```

Install additional languages:

```shell
# Ubuntu/Debian
sudo apt install tesseract-ocr-fra tesseract-ocr-deu

# macOS
brew install tesseract-lang
```

## Page Segmentation Modes (PSM)

```
0    Orientation and script detection (OSD) only
1    Automatic page segmentation with OSD
2    Automatic page segmentation, no OSD
3    Fully automatic page segmentation (default)
4    Assume single column of text
5    Assume single uniform block of vertically aligned text
6    Assume single uniform block of text
7    Treat image as single text line
8    Treat image as single word
9    Treat image as single word in circle
10   Treat image as single character
11   Sparse text: find as much text as possible
12   Sparse text with OSD
13   Raw line: single text line, no Tesseract hacks
```

## OCR Engine Modes (OEM)

```
0    Legacy engine only
1    Neural nets LSTM engine only
2    Legacy + LSTM engines
3    Default (based on availability)
```
