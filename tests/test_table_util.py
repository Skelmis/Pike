import pytest
from markdown_it import MarkdownIt

from pike.docx import CurrentRun, commands
from pike.structs import Table, Entry, Cell, TextAlignment


def test_table_from_csv(data_dir):
    table_1: Table = Table.from_csv_file(
        data_dir / "table.csv", column_widths=[1, 2, 3]
    )
    assert len(table_1.rows) == 3
    assert len(table_1.rows[0].cells) == 3
    assert table_1.has_header_row is True
    assert table_1.column_widths == [1, 2, 3]

    table_2: Table = Table.from_csv_file(
        data_dir / "table.csv", file_contains_headers=False
    )
    assert len(table_2.rows) == 3
    assert len(table_2.rows[0].cells) == 3
    assert table_2.has_header_row is False


def test_table_from_ast(data_dir):
    markdown = MarkdownIt().enable("table")
    ast = markdown.parse((data_dir / "table.md").read_text())
    table = Table.from_ast(ast)
    assert len(table.rows) == 4
    assert len(table.rows[0].cells) == 2
    assert table.has_header_row is True


def test_table_text_to_cell():
    cell: Cell = Table.text_to_cell("**Bold** but *italic*")
    assert len(cell.content) == 3
    assert cell.content[0].text == "Bold"
    assert cell.content[0].style == CurrentRun(bold=True)
    assert cell.content[1].text == " but "
    assert cell.content[1].style == CurrentRun()
    assert cell.content[2].text == "italic"
    assert cell.content[2].style == CurrentRun(italic=True)


def test_table_with_alignment(data_dir):
    markdown = MarkdownIt().enable("table")
    ast = markdown.parse((data_dir / "table_alignment.md").read_text())
    table = Table.from_ast(ast)
    assert len(table.rows) == 2
    assert len(table.rows[0].cells) == 4
    assert table.has_header_row is True

    assert len(table.text_alignment) == 4
    assert table.text_alignment[0] == TextAlignment.LEFT
    assert table.text_alignment[1] == TextAlignment.CENTER
    assert table.text_alignment[2] == TextAlignment.RIGHT
    assert table.text_alignment[3] == TextAlignment.NONE


def test_table_formatting(data_dir):
    markdown = MarkdownIt().enable("table")
    ast = markdown.parse((data_dir / "table_formatting.md").read_text())
    table = Table.from_ast(ast)
    assert len(table.rows) == 3
    assert len(table.rows[0].cells) == 2
    assert table.has_header_row is True

    italic = table.rows[1].cells[0]
    assert italic.content[0].text == "Italic"
    assert italic.content[0].style == CurrentRun(italic=True)

    bold = table.rows[2].cells[0]
    assert bold.content[0].text == "Bold"
    assert bold.content[0].style == CurrentRun(bold=True)

    # This is a 'hack' to ensure formatting
    # is applied on items that don't exist
    # as a CurrentRun entry.
    inline = table.rows[1].cells[1]
    assert inline.content[0].text == commands.create_command_string(
        "insert_text", "Inline", inline=True
    )

    nothing = table.rows[2].cells[1]
    assert nothing.content[0].text == "Nothing"
    assert nothing.content[0].style == CurrentRun()


def test_table_commands(data_dir):
    markdown = MarkdownIt().enable("table")
    data = (data_dir / "table_command.md").read_text()
    data = data.replace(
        "CMD",
        commands.create_command_string(
            "add_page_break",
            # for_embedding_in_markdown=False,
        ),
    )
    ast = markdown.parse(data)
    table = Table.from_ast(ast)

    assert len(table.rows) == 4
    assert len(table.rows[0].cells) == 2
    assert table.has_header_row is True

    custom_command = table.rows[2].cells[0]
    assert custom_command.content[0].text == commands.create_command_string(
        "add_page_break"
    )

    # Ensure we didn't break everything
    assert table.rows[1].cells[0].content[0].text == "Above"
    assert table.rows[1].cells[1].content[0].text == "Above right"
    assert table.rows[2].cells[1].content[0].text == "Side"
    assert table.rows[3].cells[0].content[0].text == "Bottom row"
    assert table.rows[3].cells[1].content[0].text == "Right"
