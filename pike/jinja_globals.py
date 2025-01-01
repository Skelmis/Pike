from __future__ import annotations

import logging
import typing
from io import StringIO
from pathlib import Path

from pike.docx import commands

if typing.TYPE_CHECKING:
    from pike import Engine, File

log = logging.getLogger(__name__)


def get_folder(engine: Engine, section_name: str) -> list[dict[str, typing.Any]]:
    """Given a folder name, return a list of the content"""
    data: list[dict[str, typing.Any]] = list(
        engine._folder_variables[section_name].values()
    )
    return list(sorted(data, key=lambda file: file.get("id"), reverse=False))


def comment(file: File, comment_value: str) -> str:
    """Raise a comment for review"""
    log.warning(
        "Comment: '%s'\n\tFile: %s",
        comment_value,
        file.file,
    )
    return commands.create_command_string("NOP", for_embedding_in_markdown=True)


def insert_image(
    image_src: str,
    *,
    alt_text: str = None,
    width: float = None,
    height: float = None,
    caption: str = None,
) -> str:
    """

    Parameters
    ----------
    image_src
    alt_text
    width: float
        Width in centimeters
    height: float
        Height in centimeters
    caption

    Returns
    -------

    """
    data = StringIO()

    data.write(f"<img src='{image_src}'")
    if alt_text:
        data.write(f" alt='{alt_text}'")
    if width:
        data.write(f" width='{width}'")
    if height:
        data.write(f" height='{height}'")
    if caption:
        data.write(f" title='{caption}'")
    data.write(">")
    return data.getvalue()
