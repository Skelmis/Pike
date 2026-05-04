import time
from pathlib import Path

from pike import Engine, File, structs


def main():
    start = time.time()
    engine = Engine.load_from_configuration(
        Path("."),
        excluded_paths=["README.md", ".venv"],
        configuration=structs.ConfigT(),
        variables={"title": "Virtual Configuration Report"},
    )
    engine.docx_header = "**Example Report**"
    engine.docx_footer = "Example Footers\tMiddle\tRight"
    engine.run()
    end = time.time()
    print(f"Runtime: {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
