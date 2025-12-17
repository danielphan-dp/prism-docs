# ocr-multi-lang

OCR mixed-language documents with multiple languages simultaneously.

## Synopsis

```
prism-docs ocr-multi-lang <input> [options]
```

## Options

```
-o, --output PATH      Output text file path
--langs LANGS          Languages (+-separated or list) (default: eng+fra+deu)
--dpi N                DPI for conversion (default: 300)
--psm N                Page segmentation mode (default: 3)
```

## Examples

```shell
# English + French + German
prism-docs ocr-multi-lang document.pdf

# Custom language combination
prism-docs ocr-multi-lang document.pdf --langs eng+spa+por

# Asian languages
prism-docs ocr-multi-lang document.pdf --langs chi_sim+jpn+kor

# European mix
prism-docs ocr-multi-lang document.pdf --langs eng+fra+deu+ita+spa
```

## Common Language Combinations

```shell
# Western European
--langs eng+fra+deu+spa+ita+por

# Eastern European
--langs eng+rus+pol+ces+ukr

# East Asian
--langs chi_sim+jpn+kor

# Middle Eastern
--langs ara+heb+fas

# South Asian
--langs hin+ben+tam
```

## Notes

- Order matters: first language is primary
- More languages = slower processing
- Ensure all language packs are installed

## Install Language Packs

```shell
# Ubuntu/Debian
sudo apt install tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-spa

# List available
apt-cache search tesseract-ocr-

# macOS (all languages)
brew install tesseract-lang
```

## Requirements

- `uv sync --extra ocr`
- Tesseract OCR with required language packs

## See Also

- [ocr-detect-lang](ocr-detect-lang.md) - Auto-detect language
- [ocr](ocr.md) - Single language OCR
