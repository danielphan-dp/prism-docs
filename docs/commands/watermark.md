# watermark

Add a watermark to PDF pages.

## Synopsis

```
prism-docs watermark <input> <watermark> [options]
```

## Options

```
-o, --output PATH      Output file path
--layer LAYER          Watermark layer: above, below (default: below)
```

## Examples

```shell
# Add watermark below content
prism-docs watermark document.pdf logo.pdf

# Add watermark above content
prism-docs watermark document.pdf stamp.pdf --layer above

# Specify output
prism-docs watermark document.pdf watermark.pdf -o marked.pdf
```

## See Also

- [stamp](stamp.md) - Add text stamp to pages
- [overlay](overlay.md) - Overlay PDF on another
