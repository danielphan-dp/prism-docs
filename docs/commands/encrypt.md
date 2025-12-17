# encrypt

Encrypt a PDF file with password protection.

## Synopsis

```
prism-docs encrypt <input> <password> [options]
```

## Options

```
-o, --output PATH      Output file path
--algorithm ALGO       Encryption algorithm (default: AES-256)
```

## Examples

```shell
# Basic encryption
prism-docs encrypt document.pdf mypassword

# Specify output file
prism-docs encrypt document.pdf mypassword -o secured.pdf

# Use specific algorithm
prism-docs encrypt document.pdf mypassword --algorithm AES-128
```

## Notes

- AES algorithms use `cryptography`.

## See Also

- [decrypt](decrypt.md) - Decrypt PDF files
- [permissions](permissions.md) - Set PDF permissions
