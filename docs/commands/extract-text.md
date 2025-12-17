# extract-text

Extract text content from PDF files.

## Synopsis

```
prism-docs extract-text <input>... [options]
```

## Options

```
--separator STR        Separator between files (default: \n\n)
```

## Examples

```shell
# Extract from single file
prism-docs extract-text document.pdf

# Extract from multiple files
prism-docs extract-text file1.pdf file2.pdf

# Custom separator
prism-docs extract-text *.pdf --separator "---\n"

# Redirect to file
prism-docs extract-text document.pdf > content.txt
```

## See Also

- [info](info.md) - View PDF metadata
