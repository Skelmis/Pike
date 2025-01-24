import json
import shutil
from pathlib import Path
from typing import Annotated

import typer

from pike import Engine

app = typer.Typer()


@app.command()
def run(
    report_directory: Annotated[
        Path,
        typer.Argument(
            help="The base directory of the report. Defaults to current directory."
        ),
    ] = Path("."),
    load_default_plugins: Annotated[
        bool, typer.Argument(help="Whether or not to load default useful plugins")
    ] = True,
):
    """Given a folder, generate the report.

    This command is useful if you don't need to extend the engine.

    Parameters
    ----------
    report_directory: Path
        The base directory of the report. Defaults to current directory.
    load_default_plugins: bool
        Whether to load default useful plugins
    """
    engine = Engine.load_from_directory(
        report_directory, load_default_plugins=load_default_plugins
    )
    engine.run()


@app.command()
def scaffold(
    target_directory: Annotated[
        Path, typer.Argument(help="Where to generate the new report structure in.")
    ],
    title: Annotated[str, typer.Option(help="The title for this report")] = None,
    project_id: Annotated[
        str, typer.Option(help="The project id for this report")
    ] = None,
):
    """Build a new report directory with the relevant starter files.

    Parameters
    ----------
    target_directory: Path
        Where to generate the new report structure in.
    title: str|None
        The title for this report
    project_id: str|None
        The project id for this report
    """
    target_directory.mkdir(exist_ok=True, parents=True)
    config_dir = target_directory / "configuration"
    config_dir.mkdir(exist_ok=True, parents=True)
    content_dir = target_directory / "content"
    content_dir.mkdir(exist_ok=True, parents=True)
    with open(content_dir / "one.md") as f:
        f.write("---\nid: one\n---\n# Title {{ id }}\n\nContent for file {{ id }}")
    with open(content_dir / "two.md") as f:
        f.write("---\nid: two\n---\n# Title {{ id }}\n\nContent for file {{ id }}")
    with open(config_dir / "layout.md") as f:
        f.write(
            "{% for file in get_folder('content') %}\n{{ file.content }}\n{% endfor %}"
        )
    data = {}
    if title is not None:
        data["title"] = title
    if project_id is not None:
        data["project_id"] = project_id
    with open(config_dir / "variables.json", "w") as f:
        f.write(json.dumps(data))
    pike_path = Path(__file__).parent.parent
    shutil.copy(
        pike_path / "default_files" / "config.json",
        config_dir / "config.json",
    )


if __name__ == "__main__":
    app()
