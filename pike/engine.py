from __future__ import annotations

import shutil
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Any, Callable

import jinja2
from docx import utility
from jinja2 import Environment
from jinja2.sandbox import SandboxedEnvironment

from pike import File, checks, utils, structs, injections
from pike.docx import Docx, commands
from pike import jinja_globals as jg


class Engine:

    def __init__(
        self,
        base_directory: Path,
        *,
        configuration: structs.ConfigT,
        load_default_plugins: bool = True,
        load_default_custom_commands: bool = True,
        global_variables: dict[str, Any] = None,
    ) -> None:
        self.base_directory: Path = base_directory
        self.config_directory: Path = base_directory / "configuration"
        self.config: structs.ConfigT = configuration
        self.global_variables = global_variables

        self.files: list[File] = []
        self._layout_file: File | None = None
        self._plugins: list[Callable[[Engine], None]] = []
        self._file_plugins: dict[
            str, Callable[[File], Any] | Callable[[File, ...], Any]
        ] = {}
        self._jinja_custom_commands: dict[str, Callable[[...], ...]] = {}
        self._custom_commands_to_add: list[tuple[str, Callable[[...], ...], bool]] = []
        self._file_variables: dict[str, dict[str, Any]] = {}
        self._folder_variables: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)

        self.docx_header: str | None = None
        self.docx_footer: str | None = None

        if self.config["use_sandbox"]:
            self.jinja_env: SandboxedEnvironment | Environment = SandboxedEnvironment(
                lstrip_blocks=True,
                undefined=jinja2.StrictUndefined,
            )
        else:
            self.jinja_env: Environment = Environment(
                lstrip_blocks=True,
                undefined=jinja2.StrictUndefined,
            )

        if load_default_plugins:
            self.load_default_injections()

        if load_default_custom_commands:
            self.load_default_custom_commands()

    def add_custom_command(
        self,
        command_name: str,
        command_callable: Callable[..., ...],
        *,
        provide_docx_instance: bool = False,
    ) -> Engine:
        """Load a custom command into the Engine.

        This method will load a custom command into the Docx AST
        as well as exposing the command via Jinja to templates.

        Parameters
        ----------
        command_name: str
            The name of the command to call
        command_callable
            The relevant function to call.
        provide_docx_instance: bool
            If True (defaults to False), the docx instance will be
            provided as the first positional argument.

        Returns
        -------
        Engine
            The current Engine instance for method chaining.
        """
        self._custom_commands_to_add.append(
            (command_name, command_callable, provide_docx_instance)
        )
        self._jinja_custom_commands[command_name] = partial(
            commands.create_command_string,
            command_name,
        )
        return self

    @classmethod
    def load_from_directory(
        cls,
        base_directory: Path,
        *,
        load_default_plugins: bool = True,
    ) -> Engine:
        """Given a report on disk, load the engine.

        Parameters
        ----------
        base_directory : Path
            Where the report is located
        load_default_plugins : bool
            Whether to load the default plugins.
        """
        checks.ensure_config_exists(Path(base_directory))
        config: structs.ConfigT = utils.read_file_as_json(
            base_directory / "configuration" / "config.json"
        )
        checks.ensure_layout_exists(base_directory, config)
        variables = utils.read_file_as_json(
            base_directory / "configuration" / "variables.json",
            allow_missing=True,
        )
        global_variables = {**variables, "globals": variables}
        return cls(
            base_directory,
            load_default_plugins=load_default_plugins,
            global_variables=global_variables,
            configuration=config,
        )

    def load_default_injections(self) -> None:
        """Loads a bunch of default, useful plugins"""
        self.register_plugin(injections.raise_on_todo)

    def load_default_custom_commands(self) -> None:
        """Loads a bunch of default custom commands.

        Currently, these are:
        - add_page_break
        - insert_text
        """
        self.add_custom_command(
            "add_page_break",
            commands.insert_page_break,
            provide_docx_instance=True,
        )
        self.add_custom_command(
            "insert_text",
            commands.insert_text,
            provide_docx_instance=True,
        )
        self.add_custom_command(
            "insert_soft_break",
            commands.insert_soft_break,
            provide_docx_instance=True,
        )

    def register_plugin(self, plugin: Callable[[Engine], None]) -> Engine:
        """Register a given callable as a plugin.


        .. code-block:: python
            :linenos:


            def example_plugin(engine: Engine) -> None:
                # Do something here

            ...

            engine.register_plugin(example_plugin)


        Parameters
        ----------
        plugin: Callable[[Engine], None]
            The function to be called

        Returns
        -------
        Engine
            The current engine instance for method chaining.
        """
        self._plugins.append(plugin)
        return self

    def register_file_plugin(
        self, name: str, func: Callable[[File], Any] | Callable[[File, ...], Any]
    ) -> Engine:
        """Register a function as a plugin on every file.

        These plugins are not called by default, but rather exposed
        under the 'plugins' keyword within the Jinja template.

        .. code-block:: python
            :linenos:


            def example_plugin(file: File, name: str) -> str:
                # Do something here
                return f"Hello {name} from {file.id}"

            ...

            engine.register_file_plugin('example', example_plugin)

            ...

            {{ files.<ID>.plugins.example("Skelmis") }}

        Parameters
        ----------
        name : str
            The name of the plugin.
        func : Callable[[File], Any] | Callable[[File, ...], Any]
            The function to register under this name.
        """
        self._file_plugins[name] = func
        return self

    def inject_variables(self, content: str, variables: dict[str, Any]) -> str:
        global_vars = {
            **self._jinja_custom_commands,
            "get_folder": partial(jg.get_folder, self),
        }
        template = self.jinja_env.from_string(
            content,
            globals=global_vars,
        )
        return template.render(**variables)

    def run(self):
        self.locate_all_files()
        self.update_global_variables()

        for file in self.files:
            file.inject_variables()

        self.update_global_variables()

        for plugin in self._plugins:
            plugin(self)

        self._layout_file.inject_variables()

        output_directory = self.base_directory / self.config["output_directory"]
        output_directory.mkdir(exist_ok=True)
        output_document_name = self.inject_variables(
            self.config["output_document_name"], self.global_variables
        )

        if self.config["output_files"]["markdown"]:
            with open(
                output_directory / f"{output_document_name}.md",
                "w",
            ) as f:
                f.write(self._layout_file.content)

        if self.config["output_files"]["docx"] or self.config["output_files"]["pdf"]:
            docx = Docx(self)
            docx.import_commands_from_engine()

            docx_file = docx.create_document(
                content=self._layout_file.content,
                filename=f"{output_document_name}.docx",
            )
            shutil.move(docx_file, output_directory / f"{output_document_name}.docx")

            docx_file = output_directory / f"{output_document_name}.docx"

            if self.config["output_files"]["pdf"]:
                utility.document_to_pdf(docx_file)
                shutil.move(
                    f"{output_document_name}.pdf",
                    output_directory / f"{output_document_name}.pdf",
                )

            if not self.config["output_files"]["docx"]:
                docx_file.unlink()

    def locate_all_files(self) -> None:
        layout_file = None
        for md_file in Path(self.base_directory).rglob("*.md"):
            if (
                md_file.name == self.config["layout_file"]
                and md_file.parent == self.config_directory
            ):
                layout_file = File(md_file, engine=self, ignore_id_check=True)
            elif md_file.parent.name == self.config["output_directory"]:
                # Skip output doc if exists
                continue
            else:
                self.files.append(File(md_file, engine=self))

        if layout_file is None:
            raise ValueError("Missing layout.md")

        self._layout_file = layout_file

    def update_global_variables(self):
        # Reset before we do this so that
        # we don't end up with duplicates
        self._file_variables: dict[str, dict[str, Any]] = {}
        self._folder_variables: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)

        for file in self.files:
            self._file_variables[file.id] = file.layout_variables
            self._folder_variables[file.folder.name][file.id] = file.layout_variables

        # Mutate globals for usage
        self.global_variables["files"] = self._file_variables
        self.global_variables["folders"] = self._folder_variables
