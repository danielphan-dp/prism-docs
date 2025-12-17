# interleave

Interleave pages from two PDFs.

## Synopsis

```
prism-docs interleave <odd-pages> <even-pages> [options]
```

## Options

```
-o, --output PATH      Output file path
--reverse-second       Reverse second PDF before interleaving
```

## Examples

```shell
# Interleave two PDFs
prism-docs interleave odd.pdf even.pdf

# Reverse second (for duplex scanning)
prism-docs interleave front.pdf back.pdf --reverse-second -o combined.pdf
```

## Notes

Useful for combining separately scanned front and back pages.

## See Also

- [merge](merge.md) - Merge PDFs sequentially
