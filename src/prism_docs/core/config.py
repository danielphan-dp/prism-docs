"""Configuration management for Prism Docs."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

from prism_docs.core.types import (
    OperationConfig,
    OutputConfig,
    OutputNaming,
    OverwritePolicy,
)

CONFIG_DIR_NAME = "prism-docs"
LEGACY_CONFIG_DIR_NAME = "pdf-tools"
LOCAL_CONFIG_FILENAME = "prism-docs.yaml"
LEGACY_LOCAL_CONFIG_FILENAME = "pdf-tools.yaml"


@dataclass
class GlobalConfig:
    """Global configuration settings."""

    verbose: bool = False
    quiet: bool = False
    dry_run: bool = False
    parallel: bool = False
    max_workers: int = 4


@dataclass
class Config:
    """Main configuration container."""

    global_settings: GlobalConfig = field(default_factory=GlobalConfig)
    default_output: OutputConfig = field(default_factory=OutputConfig)
    operations: dict[str, OperationConfig] = field(default_factory=dict)

    def get_operation_config(self, operation_name: str) -> OperationConfig:
        """Get configuration for a specific operation, with defaults."""
        if operation_name in self.operations:
            return self.operations[operation_name]

        # Return default config with operation-specific suffix
        return OperationConfig(output=self.default_output)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        """Create Config from dictionary."""
        global_data = data.get("global", {})
        global_settings = GlobalConfig(
            verbose=global_data.get("verbose", False),
            quiet=global_data.get("quiet", False),
            dry_run=global_data.get("dry_run", False),
            parallel=global_data.get("parallel", False),
            max_workers=global_data.get("max_workers", 4),
        )

        default_output_data = data.get("default_output", {})
        default_output = _parse_output_config(default_output_data)

        operations = {}
        for op_name, op_data in data.get("operations", {}).items():
            operations[op_name] = OperationConfig(
                enabled=op_data.get("enabled", True),
                output=_parse_output_config(op_data.get("output", {}), default_output),
                options=op_data.get("options", {}),
            )

        return cls(
            global_settings=global_settings,
            default_output=default_output,
            operations=operations,
        )

    @classmethod
    def from_yaml(cls, path: Path | str) -> "Config":
        """Load configuration from YAML file."""
        path = Path(path)
        if not path.exists():
            return cls()

        with open(path) as f:
            data = yaml.safe_load(f) or {}

        return cls.from_dict(data)

    @classmethod
    def from_file(cls, path: Path | str) -> "Config":
        """Load configuration from file (auto-detect format)."""
        path = Path(path)
        suffix = path.suffix.lower()

        if suffix in (".yaml", ".yml"):
            return cls.from_yaml(path)
        else:
            raise ValueError(f"Unsupported config format: {suffix}")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "global": {
                "verbose": self.global_settings.verbose,
                "quiet": self.global_settings.quiet,
                "dry_run": self.global_settings.dry_run,
                "parallel": self.global_settings.parallel,
                "max_workers": self.global_settings.max_workers,
            },
            "default_output": _output_config_to_dict(self.default_output),
            "operations": {
                name: {
                    "enabled": op.enabled,
                    "output": _output_config_to_dict(op.output),
                    "options": op.options,
                }
                for name, op in self.operations.items()
            },
        }

    def to_yaml(self, path: Path | str) -> None:
        """Save configuration to YAML file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)


def _parse_output_config(
    data: dict[str, Any],
    default: OutputConfig | None = None,
) -> OutputConfig:
    """Parse output configuration from dictionary."""
    if default is None:
        default = OutputConfig()

    naming_str = data.get("naming", default.naming.value)
    naming = OutputNaming(naming_str) if isinstance(naming_str, str) else naming_str

    overwrite_str = data.get("overwrite", default.overwrite.value)
    overwrite = OverwritePolicy(overwrite_str) if isinstance(overwrite_str, str) else overwrite_str

    output_dir = data.get("output_dir")
    if output_dir:
        output_dir = Path(output_dir)

    return OutputConfig(
        naming=naming,
        suffix=data.get("suffix", default.suffix),
        prefix=data.get("prefix", default.prefix),
        fixed_name=data.get("fixed_name", default.fixed_name),
        pattern=data.get("pattern", default.pattern),
        output_dir=output_dir or default.output_dir,
        overwrite=overwrite,
    )


def _output_config_to_dict(config: OutputConfig) -> dict[str, Any]:
    """Convert OutputConfig to dictionary."""
    result: dict[str, Any] = {
        "naming": config.naming.value,
        "overwrite": config.overwrite.value,
    }

    if config.suffix:
        result["suffix"] = config.suffix
    if config.prefix:
        result["prefix"] = config.prefix
    if config.fixed_name:
        result["fixed_name"] = config.fixed_name
    if config.pattern != "{stem}{suffix}{ext}":
        result["pattern"] = config.pattern
    if config.output_dir:
        result["output_dir"] = str(config.output_dir)

    return result


def get_default_config_path() -> Path:
    """Get the default configuration file path."""
    return Path.home() / ".config" / CONFIG_DIR_NAME / "config.yaml"


def load_config(path: Path | str | None = None) -> Config:
    """Load configuration from file or return defaults."""
    if path:
        return Config.from_file(path)

    candidates = [
        get_default_config_path(),
        Path.home() / ".config" / LEGACY_CONFIG_DIR_NAME / "config.yaml",
        Path(LOCAL_CONFIG_FILENAME),
        Path(LEGACY_LOCAL_CONFIG_FILENAME),
    ]
    for candidate in candidates:
        if candidate.exists():
            return Config.from_file(candidate)

    return Config()
