# Prism Docs

CLI toolkit for PDF editing, security, OCR, and image conversion.

## Installation

```shell
git clone https://github.com/danielphan-dp/pdf-tools.git prism-docs
cd prism-docs
uv sync
```

For image operations:

```shell
uv sync --extra images
```

For OCR operations:

```shell
uv sync --extra ocr
# Also requires: sudo apt install tesseract-ocr (Linux)
```

## Quick Start

```shell
prism-docs --help
prism-docs <command> --help
```

`pdf-tools` remains available as a command alias for compatibility.

## Commands

See [docs/commands](docs/commands/README.md) for the full reference. For quick scanning, here are all CLI
subcommands with their signatures (from `prism-docs <command> --help`).

Note: global flags like `-c/--config`, `-v/--verbose`, `-q/--quiet`, `--dry-run`, `--parallel`, and
`--output-dir` apply to every command.

### Basic operations

| Command | Signature |
|---------|-----------|
| [`encrypt`](docs/commands/encrypt.md) | `prism-docs encrypt [-o OUTPUT] [--owner-password OWNER_PASSWORD] [--algorithm {RC4-40,RC4-128,AES-128,AES-256}] input password` |
| [`decrypt`](docs/commands/decrypt.md) | `prism-docs decrypt [-o OUTPUT] input password` |
| [`merge`](docs/commands/merge.md) | `prism-docs merge output inputs [inputs ...]` |
| [`watermark`](docs/commands/watermark.md) | `prism-docs watermark [-o OUTPUT] [--layer {above,below}] [--pages PAGES] input watermark` |
| [`compress`](docs/commands/compress.md) | `prism-docs compress [-o OUTPUT] inputs [inputs ...]` |
| [`metadata`](docs/commands/metadata.md) | `prism-docs metadata [--action {view,edit}] [-o OUTPUT] [--title TITLE] [--author AUTHOR] [--subject SUBJECT] input` |

### Page manipulation

| Command | Signature |
|---------|-----------|
| [`extract-pages`](docs/commands/extract-pages.md) | `prism-docs extract-pages [-o OUTPUT] [--start START] [--end END] [--pages PAGES] input` |
| [`extract-text`](docs/commands/extract-text.md) | `prism-docs extract-text [-o OUTPUT] [--separator SEPARATOR] inputs [inputs ...]` |
| [`rotate`](docs/commands/rotate.md) | `prism-docs rotate [-o OUTPUT] [--pages PAGES] input {90,180,270}` |
| [`split`](docs/commands/split.md) | `prism-docs split [--mode {pages,ranges}] [--ranges RANGES] [--output-dir OUTPUT_DIR] input` |
| [`page-numbers`](docs/commands/page-numbers.md) | `prism-docs page-numbers [-o OUTPUT] [--position {bottom-center,bottom-left,bottom-right,top-center,top-left,top-right}] [--format FORMAT] [--font-size FONT_SIZE] [--margin MARGIN] [--start START] [--skip-first] input` |
| [`stamp`](docs/commands/stamp.md) | `prism-docs stamp [-o OUTPUT] [--position {center,top-left,top-right,bottom-left,bottom-right}] [--font-size FONT_SIZE] [--rotation ROTATION] [--opacity OPACITY] [--color COLOR] [--pages PAGES] input text` |
| [`reverse`](docs/commands/reverse.md) | `prism-docs reverse [-o OUTPUT] input` |
| [`interleave`](docs/commands/interleave.md) | `prism-docs interleave [-o OUTPUT] [--reverse-second] input1 input2` |
| [`remove-pages`](docs/commands/remove-pages.md) | `prism-docs remove-pages [-o OUTPUT] input pages` |
| [`overlay`](docs/commands/overlay.md) | `prism-docs overlay [-o OUTPUT] [--pages PAGES] input overlay` |

### Image operations (requires the `images` extra)

| Command | Signature |
|---------|-----------|
| [`images-to-pdf`](docs/commands/images-to-pdf.md) | `prism-docs images-to-pdf -o OUTPUT [--page-size PAGE_SIZE] [--margin MARGIN] [--fit {contain,cover,stretch}] images [images ...]` |
| [`pdf-to-images`](docs/commands/pdf-to-images.md) | `prism-docs pdf-to-images [--output-dir OUTPUT_DIR] [--format {png,jpeg,webp}] [--dpi DPI] [--pages PAGES] input` |
| [`extract-images`](docs/commands/extract-images.md) | `prism-docs extract-images [--output-dir OUTPUT_DIR] [--format {original,png,jpeg}] [--min-size MIN_SIZE] input` |

### Security

| Command | Signature |
|---------|-----------|
| [`flatten`](docs/commands/flatten.md) | `prism-docs flatten [-o OUTPUT] [--annotations] [--forms] input` |
| [`permissions`](docs/commands/permissions.md) | `prism-docs permissions --owner-password OWNER_PASSWORD [-o OUTPUT] [--allow-print] [--allow-copy] [--allow-modify] [--allow-annotate] [--allow-forms] input` |
| [`redact`](docs/commands/redact.md) | `prism-docs redact [-o OUTPUT] [--regions REGIONS] [--text TEXT] [--color COLOR] input` |

### Utilities

| Command | Signature |
|---------|-----------|
| [`info`](docs/commands/info.md) | `prism-docs info [-v] [--json] input` |
| [`validate`](docs/commands/validate.md) | `prism-docs validate [--strict] inputs [inputs ...]` |
| [`crop`](docs/commands/crop.md) | `prism-docs crop [-o OUTPUT] [--left LEFT] [--right RIGHT] [--top TOP] [--bottom BOTTOM] [--margin MARGIN] [--percent PERCENT] [--pages PAGES] input` |
| [`resize`](docs/commands/resize.md) | `prism-docs resize [-o OUTPUT] [--size {A4,A3,A5,Letter,Legal,Tabloid}] [--width WIDTH] [--height HEIGHT] [--scale SCALE] [--fit {contain,cover,stretch}] [--pages PAGES] input` |
| [`bookmarks`](docs/commands/bookmarks.md) | `prism-docs bookmarks [--action {view,extract,add}] [-o OUTPUT] [--from-file FROM_FILE] input` |

### OCR operations (requires the `ocr` extra)

| Command | Signature |
|---------|-----------|
| [`ocr`](docs/commands/ocr/ocr.md) | `prism-docs ocr [-o OUTPUT] [--lang LANG] [--dpi DPI] [--psm PSM] [--oem OEM] [--pages PAGES] [--timeout TIMEOUT] input` |
| [`searchable-pdf`](docs/commands/ocr/searchable-pdf.md) | `prism-docs searchable-pdf [-o OUTPUT] [--lang LANG] [--dpi DPI] [--psm PSM] [--timeout TIMEOUT] input` |
| [`ocr-extract`](docs/commands/ocr/ocr-extract.md) | `prism-docs ocr-extract [-o OUTPUT] [--lang LANG] [--dpi DPI] [--psm PSM] [--preprocess {none,threshold,blur,sharpen,denoise}] [--threshold THRESHOLD] [--contrast CONTRAST] [--brightness BRIGHTNESS] [--invert] [--format {text,hocr,tsv,box,data}] input` |
| [`ocr-batch`](docs/commands/ocr/ocr-batch.md) | `prism-docs ocr-batch [--output-dir OUTPUT_DIR] [--lang LANG] [--dpi DPI] [--psm PSM] [--output-type {txt,pdf}] [--fast] inputs [inputs ...]` |
| [`ocr-data`](docs/commands/ocr/ocr-data.md) | `prism-docs ocr-data [-o OUTPUT] [--lang LANG] [--dpi DPI] [--psm PSM] [--min-confidence MIN_CONFIDENCE] [--level {word,line,block,page}] input` |
| [`ocr-detect-lang`](docs/commands/ocr/ocr-detect-lang.md) | `prism-docs ocr-detect-lang [-o OUTPUT] [--dpi DPI] [--fallback-lang FALLBACK_LANG] [--sample-pages SAMPLE_PAGES] input` |
| [`ocr-multi-lang`](docs/commands/ocr/ocr-multi-lang.md) | `prism-docs ocr-multi-lang [-o OUTPUT] [--langs LANGS] [--dpi DPI] [--psm PSM] input` |
| [`ocr-table`](docs/commands/ocr/ocr-table.md) | `prism-docs ocr-table [-o OUTPUT] [--lang LANG] [--dpi DPI] [--format {csv,tsv,json}] [--pages PAGES] input` |
| [`ocr-table-v2`](docs/commands/ocr/ocr-table-v2.md) | `prism-docs ocr-table-v2 [-o OUTPUT] [--lang LANG] [--format {csv,tsv,json,xlsx}] [--pages PAGES] [--implicit-rows] [--no-implicit-rows] [--borderless] [--no-borderless] [--min-confidence MIN_CONFIDENCE] input` |

### CLI utilities

| Command | Signature |
|---------|-----------|
| [`config`](docs/commands/config.md) | `prism-docs config {show,init,path}` |
| [`list`](docs/commands/list.md) | `prism-docs list` |

## Configuration

```shell
~/.config/prism-docs/config.yaml   # Global
./prism-docs.yaml                  # Project
```

See [docs/configuration.md](docs/configuration.md) for options.

## Python API

```python
from prism_docs import run_operation

run_operation("encrypt", "input.pdf", password="secret")
run_operation("merge", "first.pdf", output_path="out.pdf", merge_inputs=["a.pdf", "b.pdf"])
```

See [docs/api.md](docs/api.md) for full reference.

## Development

```shell
uv sync
uv run pytest
uv run ruff check src/
```
