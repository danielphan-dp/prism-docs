# rotate

Rotate PDF pages.

## Synopsis

```
prism-docs rotate <input> <degrees> [options]
```

## Arguments

```
degrees                Rotation angle: 90, 180, 270
```

## Options

```
-o, --output PATH      Output file path
--pages SPEC           Pages to rotate (default: all)
```

## Examples

```shell
# Rotate all pages 90 degrees
prism-docs rotate document.pdf 90

# Rotate specific pages
prism-docs rotate document.pdf 180 --pages 1,3,5

# Rotate page range
prism-docs rotate document.pdf 270 --pages 2-4 -o rotated.pdf
```

## See Also

- [reverse](reverse.md) - Reverse page order
