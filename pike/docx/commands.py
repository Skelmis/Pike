from __future__ import annotations

import typing
from base64 import b64decode, b64encode
from io import StringIO
from typing import Final, Any

from pydantic import BaseModel

if typing.TYPE_CHECKING:
    from pike.docx import Docx

MARKER: Final[str] = "MARK-807e2383866d289f54e35bb8b2f2918c"


class Command(BaseModel):
    command: str
    arguments: list[str]
    keyword_arguments: dict[str, str]


def _b64_encode(content: str) -> str:
    """Helper method for b64 stuff"""
    return b64encode(content.encode("utf-8")).decode("utf-8")


def _b64_decode(content: str) -> str:
    """Helper method for b64 stuff"""
    return b64decode(content, validate=True).decode("utf-8")


def parse_command_string(command: str) -> Command:
    command = command.strip()
    if (
        not command.startswith(f"<{MARKER}")
        or not command.endswith(">")
        or "ARGS" not in command
        or "KWARGS" not in command
    ):
        raise ValueError(f"Malformed command format: {command}")

    parsed_args: list[str] = []
    parsed_kwargs: dict[str, str] = {}
    command = command.removeprefix(f"<{MARKER} ").removesuffix(">")
    command, args = command.split(" ARGS ", maxsplit=1)
    args, kwargs = args.split("KWARGS", maxsplit=1)
    # args = args.split(" ") if " " in args else [args] if args else []
    for arg in args.lstrip().rstrip().split(" "):
        if not arg:
            continue

        parsed_args.append(_b64_decode(arg))

    for item in kwargs.rstrip().lstrip().split(" "):
        if not item:
            continue

        key, value = item.split("|", maxsplit=1)
        parsed_kwargs[key] = _b64_decode(value)

    return Command(
        command=command,
        arguments=parsed_args,
        keyword_arguments=parsed_kwargs,
    )


def create_command_string(
    command_name: str,
    *args: Any,
    for_embedding_in_markdown: bool = False,
    **kwargs: Any,
) -> str:
    """Format a custom command as expected by the Pike AST.

    Parameters
    ----------
    command_name: str
        The name of the command to create.
        This is how the AST knows where to pass the call to.
    args: list[str]
        A list of string arguments to pass to the command.
    for_embedding_in_markdown: bool
        The AST parser requires two \n\n to pick up on HTML blocks.

        If set to true (default false), then we add this.
    kwargs: dict[str, Any]
        A dict of keyword arguments to pass to the command.

    Notes
    -----
    All arguments will be turned into strings, it is expected
    that the command itself turns things back into required data structures.

    Returns
    -------
    str
        A formatted command string built using HTML blocks.
    """
    data = StringIO()
    data.write(f"<{MARKER} {command_name} ARGS")
    for argument in args:
        if not isinstance(argument, str):
            argument = str(argument)

        data.write(f" {_b64_encode(argument)}")

    data.write(" KWARGS")
    for key, value in kwargs.items():
        data.write(f" {key}|{_b64_encode(value)}")

    data.write(">")

    if for_embedding_in_markdown:
        data.write("\n\n")

    return data.getvalue()


def insert_page_break(docx: Docx):
    """A custom command to add a page break to the document."""
    docx.template_file.add_page_break()
