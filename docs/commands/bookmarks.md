# bookmarks

Manage PDF bookmarks (outline).

## Synopsis

```
prism-docs bookmarks <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--action ACTION        Action: view, extract, add (default: view)
--from-file PATH       File with bookmarks to add (format: title|page)
```

## Examples

```shell
# View bookmarks
prism-docs bookmarks document.pdf

# Extract bookmarks to a text file
prism-docs bookmarks document.pdf --action extract -o bookmarks.txt

# Add bookmarks from file
prism-docs bookmarks document.pdf --action add --from-file bookmarks.txt -o with-bookmarks.pdf
```

## Bookmark File Format

```
Chapter 1|1
Section 1.1|3
Section 1.2|5
Chapter 2|10
```

## See Also

- [metadata](metadata.md) - Edit metadata
- [info](info.md) - View PDF info
