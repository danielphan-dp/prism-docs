# permissions

Set PDF permissions and restrictions.

## Synopsis

```
prism-docs permissions <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--owner-password PWD   Owner password (required)
--user-password PWD    User password for opening
--allow-print          Allow printing
--allow-copy           Allow copying content
--allow-modify         Allow modifications
--allow-annotate       Allow annotations
```

## Examples

```shell
# Restrict all, allow printing
prism-docs permissions document.pdf --owner-password secret --allow-print

# Set user password with permissions
prism-docs permissions document.pdf \
  --owner-password admin123 \
  --user-password user123 \
  --allow-print \
  --allow-copy

# Full restrictions
prism-docs permissions document.pdf --owner-password secret -o restricted.pdf
```

## See Also

- [encrypt](encrypt.md) - Encrypt PDF
- [flatten](flatten.md) - Flatten interactive elements
