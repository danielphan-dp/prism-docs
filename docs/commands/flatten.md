# flatten

Flatten PDF annotations and form fields.

## Synopsis

```
prism-docs flatten <input> [options]
```

## Options

```
-o, --output PATH      Output file path
```

## Examples

```shell
# Flatten annotations
prism-docs flatten form.pdf

# Specify output
prism-docs flatten filled-form.pdf -o flattened.pdf
```

## Notes

Converts interactive elements (forms, annotations) to static content.

## See Also

- [permissions](permissions.md) - Set PDF permissions
