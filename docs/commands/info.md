# info

Display PDF file information.

## Synopsis

```
prism-docs info <input> [options]
```

## Options

```
--verbose              Show detailed information
--json                 Output as JSON
```

## Examples

```shell
# Basic info
prism-docs info document.pdf

# Detailed info
prism-docs info document.pdf --verbose

# JSON output for scripting
prism-docs info document.pdf --json | jq '.pages'
```

## See Also

- [metadata](metadata.md) - View/edit metadata
- [validate](validate.md) - Validate PDF structure
