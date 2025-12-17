# stamp

Add text stamp to PDF pages.

## Synopsis

```
prism-docs stamp <input> <text> [options]
```

## Options

```
-o, --output PATH      Output file path
--rotation DEG         Text rotation in degrees (default: 45)
--opacity FLOAT        Text opacity 0.0-1.0 (default: 0.3)
--color COLOR          Text color (default: red)
--font-size SIZE       Font size (default: 48)
```

## Examples

```shell
# Add CONFIDENTIAL stamp
prism-docs stamp document.pdf "CONFIDENTIAL"

# Custom rotation and opacity
prism-docs stamp document.pdf "DRAFT" --rotation 0 --opacity 0.5

# Styled stamp
prism-docs stamp document.pdf "COPY" --color gray --font-size 72
```

## See Also

- [watermark](watermark.md) - Add PDF watermark
- [page-numbers](page-numbers.md) - Add page numbers
