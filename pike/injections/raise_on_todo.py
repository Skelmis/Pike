from __future__ import annotations

import logging
import typing

if typing.TYPE_CHECKING:
    from pike import Engine


log = logging.getLogger(__name__)


def raise_on_todo(engine: Engine) -> None:
    """Logs warnings for all found TODO's in a given file"""  # noqa
    for file in engine.files:
        for line in file.content.splitlines():
            todo_pos = line.lower().find("todo")
            if todo_pos != -1:
                todo_contents = line[todo_pos:]
                log.warning("TODO found: '%s'\n\tFile: %s", todo_contents, file.file)

        for k, v in file.variables.items():
            if (isinstance(v, str) and "todo" in v.lower()) or (
                isinstance(v, list) and any("todo" in str(i).lower() for i in v)
            ) or (not isinstance (v, list) and "todo" in str(v).lower()):
                if isinstance(v, list):
                    for item in v:
                        if "todo" in str(item).lower():
                            v = item

                log.warning(
                    "TODO found: '%s'\n\tFile: %s\n\tFrontmatter key: %s",
                    str(v).lower(),
                    file.file,
                    k,
                )
