import time
from pathlib import Path

from pike import Engine, File


def get_referenced_files(file: File) -> list[File]:
    """Get all files that reference the current one."""
    data: list[File] = []
    for f in file.engine.files:
        if f == file:
            continue

        references = f.variables.get("references")
        if references is not None:
            if file.id in references:
                data.append(f)

    return data


def main():
    start = time.time()
    engine = Engine.load_from_directory(Path("."))
    engine.register_file_plugin("get_referenced_files", get_referenced_files)
    engine.run()
    end = time.time()
    print(f"Runtime: {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
