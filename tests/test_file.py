import jinja2
import pytest
from jinja2 import UndefinedError

from pike import File, Engine


def test_basic_variable_injection(
    set_test_directory_to_example_report,
    example_report_dir,
):
    engine = Engine.load_from_directory(example_report_dir)
    file = File(example_report_dir / "title_page.md", engine=engine)

    # A patch while we wait for #1 to be resolved
    file.content = "{{info.name}}"
    assert file.content.count("{{") == 1

    with pytest.raises(UndefinedError):
        file.inject_variables()

    file.variables["info"] = {}
    file.variables["info"]["name"] = "Skelmis"
    file.inject_variables()
    assert file.content.count("{{") == 0
    assert file.content == "Skelmis"


def test_basic_variable_injection_failure(
    set_test_directory_to_example_report,
    example_report_dir,
):
    engine = Engine.load_from_directory(example_report_dir)
    file = File(example_report_dir / "title_page.md", engine=engine)

    # A patch while we wait for #1 to be resolved
    file.content = "{{name}}"
    assert file.content.count("{{") == 1

    with pytest.raises(jinja2.exceptions.UndefinedError):
        file.inject_variables()
