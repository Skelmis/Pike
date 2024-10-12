from __future__ import annotations

import logging
import typing

if typing.TYPE_CHECKING:
    from pike import Engine


log = logging.getLogger(__name__)


def raise_on_xxx(engine: Engine) -> None:
    """Logs warnings for all found XXX's in a given file"""
    for file in engine.files:
        for line in file.content.splitlines():
            xxx_pos = line.lower().find("xxx")
            if xxx_pos != -1:
                xxx_contents = line[xxx_pos:]
                log.warning("XXX found: '%s'\n\tFile: %s", xxx_contents, file.file)
