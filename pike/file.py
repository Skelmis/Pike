from __future__ import annotations

import typing as t
from functools import partial
from pathlib import Path

from pike import utils
from pike import jinja_globals as jg

if t.TYPE_CHECKING:
    from pike import Engine


class File:
    def __init__(self, file: Path, *, engine: Engine, ignore_id_check: bool = False):
        self.engine: Engine = engine
        self.file: Path = file
        self.folder: Path = file.parent
        self.content, self.variables = utils.read_file(self.file)
        self._plugins: dict[
            str, t.Callable[[File], t.Any] | t.Callable[[File, ...], t.Any]
        ] = engine._file_plugins  # noqa
        self._injections: dict[str, t.Callable[[File, ...], t.Any]] = {
            "comment": partial(jg.comment, self)
        }

        # TODO Create a test for this once virtual configurations
        #      are a supported method of File object creation
        if not ignore_id_check and "id" not in self.variables:
            raise ValueError(
                f"All files require an 'id' parameter.\n\tFile: {self.file}"
            )

    def __repr__(self) -> str:
        return f"<File '{self.file}'>"

    def __eq__(self, other):
        if not isinstance(other, File):
            return File

        try:
            return self.id == other.id
        except ValueError:
            return id(self) == id(other)

    @property
    def id(self) -> str:
        if (
            self.file.name == self.engine.config["layout_file"]
            and self.file.parent == self.engine.config_directory
        ):
            return self.file.name

        _id = self.variables.get("id")
        if _id is None:
            raise ValueError(f"{self.file} is missing a frontmatter id")

        return _id

    @property
    def layout_variables(self) -> dict[str, t.Any]:
        return {**self.variables, "content": self.content}

    def inject_variables(self):
        """Inject Jinja tags into the current file."""
        plugins = {}
        for k, v in self._plugins.items():
            plugins[k] = partial(v, self)

        local_variables = {**self.variables, "plugins": plugins, **self._injections}
        variables = {
            **local_variables,
            **self.engine.global_variables,
            "this": local_variables,
        }

        # https://stackoverflow.com/a/34002296/13781503
        prev = self.content
        while True:
            curr = self.engine.inject_variables(prev, variables)
            if curr != prev:
                prev = curr
            else:
                self.content = curr
                break
