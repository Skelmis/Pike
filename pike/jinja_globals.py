from __future__ import annotations

import logging
import typing

if typing.TYPE_CHECKING:
    from pike import Engine, File

log = logging.getLogger(__name__)


def get_folder(engine: Engine, section_name: str) -> list[dict[str, typing.Any]]:
    """Given a folder name, return a list of the content"""
    data: list[dict[str, typing.Any]] = list(
        engine._folder_variables[section_name].values()
    )
    return list(sorted(data, key=lambda file: file.get("id"), reverse=False))


def comment(file: File, comment_value: str) -> None:
    """Raise a comment for review"""
    log.warning(
        "Comment: '%s'\n\tFile: %s",
        comment_value,
        file.file,
    )
