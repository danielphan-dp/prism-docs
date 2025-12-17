# compress

Compress PDF files to reduce size.

## Synopsis

```
prism-docs compress <input>...
```

## Examples

```shell
# Compress single file
prism-docs compress large.pdf

# Compress multiple files
prism-docs compress file1.pdf file2.pdf file3.pdf

# Using glob
prism-docs compress *.pdf
```

## Notes

Uses lossless compression. Results vary based on PDF content.
