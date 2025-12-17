# remove-pages

Remove specific pages from a PDF.

## Synopsis

```
prism-docs remove-pages <input> <pages> [options]
```

## Arguments

```
pages                  Pages to remove (e.g., 2,4,6 or 1-3)
```

## Options

```
-o, --output PATH      Output file path
```

## Examples

```shell
# Remove single page
prism-docs remove-pages document.pdf 1

# Remove multiple pages
prism-docs remove-pages document.pdf 2,4,6

# Remove page range
prism-docs remove-pages document.pdf 1-3 -o trimmed.pdf
```

## See Also

- [extract-pages](extract-pages.md) - Extract specific pages
