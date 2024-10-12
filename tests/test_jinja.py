import jinja2
import pytest

from pike import Engine, File


def test_jinja_configs(engine: Engine):
    with pytest.raises(jinja2.exceptions.UndefinedError):
        engine.jinja_env.from_string("{{missing}}").render()
