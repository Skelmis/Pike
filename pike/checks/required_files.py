from __future__ import annotations

import logging
import shutil
import sys
import typing
from pathlib import Path

if typing.TYPE_CHECKING:
    from pike import Engine, File, structs

log = logging.getLogger(__name__)


def ensure_config_exists(base_directory: Path):
    """Checks all required files exist within the project"""
    config_dir = base_directory / "configuration"
    config_dir.mkdir(exist_ok=True)

    pike_path = Path(__file__).parent.parent
    if not (config_dir / "config.json").exists():
        log.debug("Configuration file not found. Creating default")
        shutil.copy(
            pike_path / "default_files" / "config.json",
            config_dir / "config.json",
        )


def ensure_layout_exists(base_directory: Path, config: structs.ConfigT):
    config_dir = base_directory / "configuration"
    config_dir.mkdir(exist_ok=True)
    if not (config_dir / config.get("layout_file", "layout.md")).exists():
        (config_dir / "layout.md").touch(exist_ok=True)
        log.critical(
            "Missing template file. "
            "I've created one, now please go fill it in"
            "\n\tFile: %s",
            config_dir / config.get("layout_file", "layout.md"),
        )

        log.critical("Please resolve the above issues before continuing")
        sys.exit()
