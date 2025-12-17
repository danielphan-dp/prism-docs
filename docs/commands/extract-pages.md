# extract-pages

Extract specific pages from a PDF.

## Synopsis

```
prism-docs extract-pages <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--start N              Start page number
--end N                End page number
--pages SPEC           Page specification (e.g., 1,3,5-8)
```

## Examples

```shell
# Extract pages 1-5
prism-docs extract-pages document.pdf --start 1 --end 5

# Extract specific pages
prism-docs extract-pages document.pdf --pages 1,3,5-8

# Extract single page
prism-docs extract-pages document.pdf --pages 1 -o cover.pdf
```

## See Also

- [remove-pages](remove-pages.md) - Remove pages from PDF
- [split](split.md) - Split PDF into parts
