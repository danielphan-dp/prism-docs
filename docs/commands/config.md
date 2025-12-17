# config

Manage Prism Docs configuration.

## Synopsis

```
prism-docs config <action>
```

Actions:

- `show` — print the effective configuration as YAML
- `init` — create a default config file (fails if it already exists)
- `path` — print the default config path

## Examples

```shell
# Show the effective config (after loading defaults + config file)
prism-docs config show

# Print where Prism Docs expects the global config to live
prism-docs config path

# Create a default config (once)
prism-docs config init
```

## See Also

- [configuration](../configuration.md) - Config file reference
- [list](list.md) - List available operations
