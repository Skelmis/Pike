from markdown_it import MarkdownIt

from pike.docx import CurrentRun
from pike.structs import Table, Entry, Cell


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
