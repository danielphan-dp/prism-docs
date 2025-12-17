# ocr-detect-lang

Auto-detect document language and perform OCR.

## Synopsis

```
prism-docs ocr-detect-lang <input> [options]
```

## Options

```
-o, --output PATH      Output text file path
--dpi N                DPI for conversion (default: 300)
--fallback-lang LANG   Fallback language if detection fails (default: eng)
--sample-pages N       Pages to sample for detection (default: 1)
```

## Examples

```shell
# Auto-detect and OCR
prism-docs ocr-detect-lang document.pdf

# Custom fallback
prism-docs ocr-detect-lang document.pdf --fallback-lang fra

# Sample more pages for accuracy
prism-docs ocr-detect-lang book.pdf --sample-pages 3
```

## Detected Scripts

| Script | Language Code |
|--------|---------------|
| Latin | eng |
| Cyrillic | rus |
| Arabic | ara |
| Hebrew | heb |
| Han (Chinese) | chi_sim |
| Hangul (Korean) | kor |
| Hiragana/Katakana | jpn |
| Thai | tha |
| Devanagari | hin |
| Greek | ell |

## Output

Text file with detected language noted at top:

```
Detected language: fra

--- Page 1 ---
Bonjour le monde...
```

## Notes

- Uses Tesseract's OSD (Orientation and Script Detection)
- Detection based on script, not specific language
- Use `ocr-multi-lang` for known mixed documents

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR with OSD data

## See Also

- [ocr-multi-lang](ocr-multi-lang.md) - Multi-language OCR
- [ocr](ocr.md) - Basic OCR with known language
