from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from pike import Engine


def get_folder(engine: Engine, section_name: str) -> list[dict[str, typing.Any]]:
    """Given a folder name, return a list of the content"""
    return list(
        sorted(
            engine._folder_variables[section_name],  # noqa
            key=lambda file: file.get("id", None),
            reverse=False,
        ),
    )

def comment(comment_value: str) -> None:
    """Raise a comment for review"""