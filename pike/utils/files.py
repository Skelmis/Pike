import json
import logging
from pathlib import Path
from typing import Any

import frontmatter

log = logging.getLogger(__name__)


def read_file_as_json(
    file: Path | str, *, allow_missing: bool = False
) -> dict[str, Any]:
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        if allow_missing:
            log.warning("Could not find file %s but defaulting to empty dict", file)
            return {}

        raise

    return data


def read_file(file: Path | str) -> tuple[str, dict[str, Any]]:
    with open(file, "r") as f:
        metadata, content = frontmatter.parse(f.read())

    return content, metadata
