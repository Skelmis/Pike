from unittest.mock import Mock, call

from docx import Document

from pike import Engine, File, utils
from pike.docx import Docx


def test_nested_blockquote_doesnt_crash(engine: Engine, data_dir) -> None:
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "nested_blockquote.md").read_text())
    docx.walk_ast(Document(), ast)


def test_line_break(engine: Engine, data_dir) -> None:
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "line_break.md").read_text())
    document = Mock()
    docx.walk_ast(document, ast)
    assert document.mock_calls == [
        call.add_paragraph(),
        call.add_paragraph().add_run("Line break:"),
        call.add_paragraph().add_run(),
        call.add_paragraph().add_run().add_break(),
        call.add_paragraph().add_run("This is the first line."),
        call.add_paragraph().add_run(),
        call.add_paragraph().add_run().add_break(),
        call.add_paragraph().add_run("And this is the second line."),
    ]


def test_paragraphs(engine: Engine, data_dir) -> None:
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "paragraphs.md").read_text())
    document = Mock()
    docx.walk_ast(document, ast)
    assert document.mock_calls == [
        call.add_paragraph(),
        call.add_paragraph().add_run("I really like using Markdown."),
        call.add_paragraph(),
        call.add_paragraph().add_run(
            "I think I'll use it to format all of my documents from now on."
        ),
    ]
