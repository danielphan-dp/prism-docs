# validate

Validate PDF file structure.

## Synopsis

```
prism-docs validate <input> [options]
```

## Options

```
--strict               Enable strict validation
```

## Examples

```shell
# Basic validation
prism-docs validate document.pdf

# Strict validation
prism-docs validate document.pdf --strict
```

## Exit Codes

```
0    Valid PDF
1    Invalid or corrupted PDF
```

## See Also

- [info](info.md) - View PDF information
