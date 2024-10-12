from pathlib import Path

import pytest

from pike import Engine


@pytest.fixture
def example_report_dir() -> Path:
    if Path("example_report").exists():
        path = Path("example_report").absolute()
    else:
        path = Path("../example_report").absolute()

    return path


@pytest.fixture
def set_test_directory_to_example_report(monkeypatch, example_report_dir):
    monkeypatch.chdir(example_report_dir)


@pytest.fixture
def engine(set_test_directory_to_example_report, example_report_dir):
    return Engine.load_from_directory(example_report_dir)
