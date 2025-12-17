# page-numbers

Add page numbers to PDF.

## Synopsis

```
prism-docs page-numbers <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--position POS         Position: bottom-center, bottom-left, bottom-right,
                       top-center, top-left, top-right (default: bottom-center)
--format FMT           Number format (default: "Page {n}")
--start N              Starting number (default: 1)
```

## Examples

```shell
# Add page numbers at bottom center
prism-docs page-numbers document.pdf

# Custom position and format
prism-docs page-numbers document.pdf --position top-right --format "{n}"

# Start from specific number
prism-docs page-numbers document.pdf --start 5 --format "Page {n} of 100"
```

## See Also

- [stamp](stamp.md) - Add text stamp
