# crop

Crop PDF page margins.

## Synopsis

```
prism-docs crop <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--margin N             Uniform margin to crop (points)
--left N               Left margin
--right N              Right margin
--top N                Top margin
--bottom N             Bottom margin
```

## Examples

```shell
# Crop uniform margin
prism-docs crop document.pdf --margin 36

# Crop specific sides
prism-docs crop document.pdf --left 72 --right 72

# Crop all sides differently
prism-docs crop document.pdf \
  --top 36 --bottom 36 \
  --left 72 --right 72 \
  -o cropped.pdf
```

## Notes

1 inch = 72 points

## See Also

- [resize](resize.md) - Resize pages
