# overlay

Overlay one PDF on another.

## Synopsis

```
prism-docs overlay <base> <overlay> [options]
```

## Options

```
-o, --output PATH      Output file path
```

## Examples

```shell
# Overlay PDF
prism-docs overlay base.pdf header.pdf

# With output path
prism-docs overlay document.pdf letterhead.pdf -o final.pdf
```

## See Also

- [watermark](watermark.md) - Add watermark
- [stamp](stamp.md) - Add text stamp
