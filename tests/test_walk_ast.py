from unittest.mock import Mock, call

from docx import Document
from docx.text.run import Run

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


def test_multiple_ordered_lists(engine: Engine, data_dir) -> None:
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "ordered_lists.md").read_text())
    document = Mock()
    docx.walk_ast(document, ast)
    assert document.mock_calls == [
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().restart_numbering(),
        call.add_paragraph().add_run("First item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Second item"),
        call.add_paragraph(),
        call.add_paragraph().add_run("Next list:"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().restart_numbering(),
        call.add_paragraph().add_run("First item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Second item"),
    ]


def test_ordered_list_nested_restarting(engine: Engine, data_dir) -> None:
    """Odd edge case, restarted the first two ordered lists fine but not nested"""
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "multi_ordered_list.md").read_text())
    document = Mock()
    docx.walk_ast(document, ast)
    assert document.mock_calls == [
        call.add_paragraph(),
        call.add_paragraph().add_run("Ordered lists:"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().restart_numbering(),
        call.add_paragraph().add_run("First item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Second item"),
        call.add_paragraph(),
        call.add_paragraph().add_run("Different markdown, same list result:"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().restart_numbering(),
        call.add_paragraph().add_run("First item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Second item"),
        call.add_paragraph(),
        call.add_paragraph().add_run("Unordered lists:"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("First item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Second item"),
        call.add_paragraph(),
        call.add_paragraph().add_run("Nested lists:"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().restart_numbering(),
        call.add_paragraph().add_run("First item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Second item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Third item"),
        call.add_paragraph(style="List Paragraph 2"),
        call.add_paragraph().add_run("Indented item"),
        call.add_paragraph(style="List Paragraph 2"),
        call.add_paragraph().add_run("Indented item"),
        call.add_paragraph(style="List Paragraph"),
        call.add_paragraph().add_run("Fourth item"),
    ]


def test_inline_code(engine: Engine, data_dir) -> None:
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "inline_code.md").read_text())
    document = Mock()
    docx.walk_ast(document, ast)
    assert document.mock_calls == [
        call.add_paragraph(),
        call.add_paragraph().add_run(style="Subtle Reference"),
        call.add_paragraph().add_run().add_text("code"),
    ]


def test_horizontal_rule(engine: Engine, data_dir) -> None:
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "horizontal_rule.md").read_text())
    document = Mock()
    docx.walk_ast(document, ast)
    assert document.mock_calls == [
        call.add_paragraph(),
        call.add_paragraph().insert_horizontal_rule(),
        call.add_paragraph(),
        call.add_paragraph().insert_horizontal_rule(),
        call.add_paragraph(),
        call.add_paragraph().insert_horizontal_rule(),
    ]
