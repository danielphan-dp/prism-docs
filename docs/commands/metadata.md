# metadata

View or edit PDF metadata.

## Synopsis

```
prism-docs metadata <input> [options]
```

## Options

```
--action ACTION        Action: view, edit (default: view)
--title STR            Set document title
--author STR           Set document author
--subject STR          Set document subject
--creator STR          Set creator application
```

## Examples

```shell
# View metadata
prism-docs metadata document.pdf

# Edit metadata
prism-docs metadata document.pdf --action edit --title "My Document"

# Set multiple fields
prism-docs metadata document.pdf --action edit \
  --title "Report" \
  --author "John Doe" \
  --subject "Q4 Analysis"
```

## See Also

- [info](info.md) - View PDF information
