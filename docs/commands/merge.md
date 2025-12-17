# merge

Merge multiple PDF files into one.

## Synopsis

```
prism-docs merge <output> <input>...
```

## Examples

```shell
# Merge two files
prism-docs merge combined.pdf first.pdf second.pdf

# Merge multiple files
prism-docs merge all.pdf chapter1.pdf chapter2.pdf chapter3.pdf

# Using glob patterns
prism-docs merge book.pdf chapters/*.pdf
```

## See Also

- [split](split.md) - Split PDF into parts
- [interleave](interleave.md) - Interleave pages from two PDFs
