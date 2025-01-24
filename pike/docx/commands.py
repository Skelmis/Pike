from __future__ import annotations

import logging
import re
import typing
from base64 import b64decode, b64encode
from io import StringIO
from typing import Final, Any

import commons
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from pydantic import BaseModel

from pike.docx import CurrentRun

if typing.TYPE_CHECKING:
    from pike.docx import Docx

log = logging.getLogger(__name__)
MARKER: Final[str] = "MARK-807e2383866d289f54e35bb8b2f2918c"
COMMAND_REGEX: Final[re.Pattern] = re.compile(rf"(<{MARKER}.*?>)")


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
        raise ValueError(f"Malformed command format: {repr(command)}")

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

        item = _b64_decode(item)
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
        if not isinstance(value, str):
            value = str(value)

        entry = _b64_encode(f"{key}|{_b64_encode(value)}")
        data.write(f" {entry}")

    data.write(">")

    return data.getvalue()


def split_str_into_command_blocks(text: str) -> list[str | Command]:
    """Given text, return commands + raw content

    Parameters
    ----------
    text: str
        The text which may or may not contain commands
    """
    data: list[str | Command] = []
    for entry in re.split(COMMAND_REGEX, text):
        if entry == "":
            continue

        try:
            data.append(parse_command_string(entry))
        except ValueError:
            data.append(entry)

    return data


def insert_page_break(docx: Docx):
    """A custom command to add a page break to the document."""
    docx.template_file.add_page_break()


def insert_soft_break(docx: Docx):
    """Inserts a new soft break, essentially hitting enter."""
    if docx.current_paragraph is None:
        # Unsure why this is None here...
        docx.current_paragraph = docx.current_paragraph = (
            docx.template_file.add_paragraph()
        )
    else:
        # Else otherwise it'd be a double up it seems
        docx.current_paragraph.add_run().add_break()


def insert_text(
    docx: Docx,
    text: str,
    *,
    inline: bool = None,
    bold: bool = None,
    italic: bool = None,
    highlight: bool = None,
    underline: bool = None,
    style: str = None,
):
    """A custom command to add a text block to the document.

    Parameters
    ----------
    docx: Docx
        The docx instance
    text: str
        What to write.
    inline: bool
        Should this be a code inline?
    bold: bool
        Should this be bold text?
    italic: bool
        Should this be italic?
    highlight: bool
        Should this be highlighted?
    underline: bool
        Should this be underlined?
    style: str
        The style to use for the given text.

        Cannot be used in conjunction with inline.
    """
    bold = commons.value_to_bool(bold)
    inline = commons.value_to_bool(inline)
    italic = commons.value_to_bool(italic)
    highlight = commons.value_to_bool(highlight)
    underline = commons.value_to_bool(underline)

    if style is not None and inline is True:
        raise ValueError("Style and Inline are mutually exclusive.")

    current_run: CurrentRun = CurrentRun(
        bold=bold, italic=italic, highlight=highlight, underline=underline
    )
    current_paragraph: Paragraph | Run | None = (
        docx.current_paragraph
        if docx.current_paragraph is not None
        else docx.template_file.add_paragraph()
    )

    if style is not None:
        current_paragraph.style = style

    if inline is True:
        # Inline code block
        if isinstance(current_paragraph, Run):
            current_paragraph.style = docx.engine.config["styles"]["inline_code"]
        else:
            current_paragraph = current_paragraph.add_run(
                style=docx.engine.config["styles"]["inline_code"]
            )

    docx.add_text(
        text,
        paragraph=current_paragraph,
        document=docx.template_file,
        current_run=current_run,
    )
