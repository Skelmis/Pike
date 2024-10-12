from pathlib import Path

from markdown_it import MarkdownIt


def test_to_ast():
    markdown = MarkdownIt().enable("table")
    markdown.options["html"] = True
    ast = markdown.parse("# Heading")
    r_1 = ast[0]
    assert r_1.type == "heading_open"


def test_tables(data_dir: Path):
    markdown = MarkdownIt().enable("table")
    ast = markdown.parse((data_dir / "table.md").read_text())
    assert len(ast) == 38


def test_table_no_header(data_dir: Path):
    markdown = MarkdownIt().enable("table")
    ast = markdown.parse((data_dir / "table_no_header.md").read_text())
    assert len(ast) == 3  # it doesnt register as a table
