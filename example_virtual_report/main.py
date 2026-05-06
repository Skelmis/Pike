import time
from pathlib import Path

from pike import Engine, File, structs


def main():
    start = time.time()
    engine = Engine.load_from_configuration(
        Path("."),
        excluded_paths=["README.md", ".venv"],
        configuration=structs.ConfigT(
            output_files=structs.OutputDocumentsT(markdown=False, pdf=False, docx=False)
        ),
        variables={"title": "Virtual Configuration Report"},
    )
    engine.docx_header = "**Example Report**"
    engine.docx_footer = "Example Footers\tMiddle\tRight"
    engine.require_layout_file = False  # TODO: Manually saving document
    engine.run()

    end = time.time()
    print(f"Runtime: {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
