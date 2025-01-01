import jinja2
import pytest

from pike import Engine, File
from pike.jinja_globals import insert_image


def test_jinja_configs(engine: Engine):
    with pytest.raises(jinja2.exceptions.UndefinedError):
        engine.jinja_env.from_string("{{missing}}").render()


def test_insert_image(engine: Engine):
    r_1 = insert_image("cat.jpg")
    assert r_1 == "<img src='cat.jpg'>"

    r_2 = insert_image("cat.jpg", width=100)
    assert r_2 == "<img src='cat.jpg' width='100'>"

    r_3 = insert_image(
        "cat.jpg", width=100, height=100, alt_text="Alt Text", caption="Caption"
    )
    assert (
        r_3
        == "<img src='cat.jpg' alt='Alt Text' width='100' height='100' title='Caption'>"
    )
