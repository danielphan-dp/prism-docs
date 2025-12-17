# Configuration

Prism Docs uses YAML configuration files for customizing behavior.

## Config Locations

```
~/.config/prism-docs/config.yaml    # Global config
./prism-docs.yaml                   # Project config (takes precedence)
```

## CLI Options

```shell
prism-docs [options] <command> [command-options]

Options:
  -c, --config PATH    Path to configuration file
  -v, --verbose        Enable verbose output
  -q, --quiet          Suppress output
  --dry-run            Show what would be done
  --parallel           Process multiple files in parallel
  --output-dir PATH    Directory for output files
```

## Config File

```yaml
global:
  verbose: false
  parallel: true
  max_workers: 4

default_output:
  naming: suffix        # suffix, prefix, fixed, custom
  overwrite: overwrite  # overwrite, skip, rename, error

operations:
  encrypt:
    output:
      suffix: "-encrypted"
    options:
      algorithm: AES-256

  compress:
    output:
      suffix: "-compressed"
      output_dir: ./compressed

  watermark:
    output:
      suffix: "-watermarked"
    options:
      layer: below
```

## Output Naming

| Mode | Description |
|------|-------------|
| `suffix` | Append suffix: `file.pdf` → `file-encrypted.pdf` |
| `prefix` | Prepend prefix: `file.pdf` → `encrypted-file.pdf` |
| `fixed` | Use fixed name (with counter for multiple) |
| `custom` | Custom pattern with variables |

## Overwrite Behavior

| Mode | Description |
|------|-------------|
| `overwrite` | Replace existing files |
| `skip` | Skip if output exists |
| `rename` | Add number: `file-1.pdf` |
| `error` | Fail if output exists |

## Per-Operation Config

Each operation can have:

```yaml
operations:
  <operation-name>:
    output:
      suffix: string
      prefix: string
      output_dir: path
    options:
      # operation-specific options
```

## Environment Variables

```shell
PRISM_DOCS_CONFIG=/path/to/config.yaml
PRISM_DOCS_VERBOSE=1
PRISM_DOCS_QUIET=1
```
