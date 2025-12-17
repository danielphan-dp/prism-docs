# decrypt

Decrypt a password-protected PDF file.

## Synopsis

```
prism-docs decrypt <input> <password> [options]
```

## Options

```
-o, --output PATH      Output file path
```

## Examples

```shell
# Decrypt to new file
prism-docs decrypt secured.pdf mypassword

# Specify output
prism-docs decrypt secured.pdf mypassword -o unlocked.pdf
```

## See Also

- [encrypt](encrypt.md) - Encrypt PDF files
