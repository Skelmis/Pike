import json
from pathlib import Path
from typing import Any

import frontmatter


def read_file_as_json(file: Path | str) -> dict[str, Any]:
    with open(file, "r") as f:
        data = json.load(f)

    return data


def read_file(file: Path | str) -> tuple[str, dict[str, Any]]:
    with open(file, "r") as f:
        metadata, content = frontmatter.parse(f.read())

    return content, metadata
