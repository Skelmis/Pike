from base64 import b64decode, b64encode
from io import StringIO
from typing import Final, Any

from pydantic import BaseModel

MARKER: Final[str] = '807e2383866d289f54e35bb8b2f2918c'

class Command(BaseModel):
    command: str
    arguments: list[str]

def parse_command_string(command: str) -> Command:
    if not command.startswith(f"<{MARKER}") and not command.endswith(">"):
        raise ValueError(f"Malformed command format: {command}")

    parsed_args:list[str] = []
    command = command.removeprefix(f"<{MARKER} ").removesuffix(">")
    try:
        command, args = command.split(" ", maxsplit=1)
        for arg in args.split(" "):
            parsed_args.append(b64decode(arg, validate=True).decode())
    except ValueError:
        # No arguments provided so no further action needed
        pass

    return Command(command=command, arguments=parsed_args)

def create_command_string(command_name: str, *args: Any) -> str:
    """Format a custom command as expected by the Pike AST.

    Parameters
    ----------
    command_name: str
        The name of the command to create.
        This is how the AST knows where to pass the call to.
    args: list[str]
        A list of string arguments to pass to the command.

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
    data.write(f"<{MARKER} {command_name}")
    for argument in args:
        if not isinstance(argument, str):
            argument = str(argument)

        data.write(f" {b64encode(argument.encode()).hex()}")
    data.write(">")
    return data.getvalue()