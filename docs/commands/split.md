# split

Split PDF into multiple files.

## Synopsis

```
prism-docs split <input> [options]
```

## Options

```
--mode MODE            Split mode: pages, ranges (default: pages)
--ranges SPEC          Range specification for ranges mode
--output-dir PATH      Output directory
```

## Examples

```shell
# Split into individual pages
prism-docs split document.pdf

# Split into page ranges
prism-docs split document.pdf --mode ranges --ranges 1-3,4-6,7-10

# Specify output directory
prism-docs split document.pdf --output-dir ./chapters
```

## See Also

- [merge](merge.md) - Merge PDF files
- [extract-pages](extract-pages.md) - Extract specific pages
