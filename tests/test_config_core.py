from pathlib import Path

from prism_docs.core.config import Config, GlobalConfig, OutputConfig, OverwritePolicy, load_config


def test_config_to_from_dict_roundtrip(tmp_path: Path) -> None:
    data = {
        "global": {
            "verbose": True,
            "quiet": False,
            "dry_run": True,
            "parallel": True,
            "max_workers": 2,
        },
        "default_output": {
            "naming": "prefix",
            "prefix": "p-",
            "overwrite": "rename",
        },
        "operations": {
            "compress": {
                "enabled": True,
                "output": {"suffix": "-c"},
                "options": {"compress_streams": False},
            }
        },
    }

    cfg = Config.from_dict(data)
    assert cfg.global_settings.verbose
    assert cfg.default_output.prefix == "p-"
    assert cfg.operations["compress"].output.suffix == "-c"

    cfg_dict = cfg.to_dict()
    assert cfg_dict["global"]["parallel"] is True
    assert cfg_dict["operations"]["compress"]["options"]["compress_streams"] is False


def test_load_config_missing_returns_default(tmp_path: Path) -> None:
    # Point to a non-existent file
    dummy = tmp_path / "nope.yaml"
    cfg = load_config(dummy)
    assert isinstance(cfg, Config)
    assert cfg.global_settings.verbose is False


def test_output_config_overwrite_policy(tmp_path: Path) -> None:
    out = OutputConfig(overwrite=OverwritePolicy.OVERWRITE)
    target = tmp_path / "a.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.touch()
    # Should allow overwrite without raising
    resolved = out.resolve_output_path(target, "sfx")
    assert resolved.name == "a-sfx.pdf"
