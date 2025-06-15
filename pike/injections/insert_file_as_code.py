from io import StringIO
from pathlib import Path

from pike import File


def insert_file_as_code(file: File, path: Path | str) -> str:
    path = (file.engine.base_directory / path).absolute()

    code = StringIO()
    code.write("```\n")
    code.write(path.read_text())
    code.write("\n```\n")
    return code.getvalue()
