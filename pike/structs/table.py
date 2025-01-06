from __future__ import annotations

import csv
from enum import Enum
from pathlib import Path

from markdown_it.token import Token
from pydantic import BaseModel

from pike import utils
from pike.docx import CurrentRun, TableContext


class TextAlignment(Enum):
    """How to align text in columns"""

    LEFT = 1
    CENTER = 2
    RIGHT = 3


class Entry(BaseModel):
    """A piece of text within a cell"""

    text: str
    """The text"""
    style: CurrentRun
    """How to style it"""

    class Config:
        arbitrary_types_allowed = True


class Cell(BaseModel):
    # Stupid nesting to support
    # multiple styles in content
    """A cell, composed of various text pieces"""
    content: list[Entry]
    """Said text pieces"""


class Row(BaseModel):
    """The cells within a given row"""

    cells: list[Cell]
    """Said cells"""


class Table:
    def __init__(
        self,
        rows: list[Row],
        *,
        has_header_row: bool = True,
        column_widths: list[float] = None,
        text_alignment: list[TextAlignment] = None,
    ):
        """Handles basic tables.

        If you want merged cells, etc. Make a custom command.

        Parameters
        ----------
        rows: list[Row]
            The rows this table exists as
        has_header_row: bool
            Whether the first Row should be ignored on insertion.
            We do this because the AST requires tables to have
            a header row even if we don't need one in the data

            Defaults to putting in the header row
        column_widths: list[float]
            A list of table column widths
        text_alignment: list[TextAlignment]
            How should a given columns text be aligned?

            Defaults to letting docx decide
        """
        self.rows: list[Row] = rows
        if not has_header_row:
            # Toss it so we don't need to check later
            self.rows.pop(0)

        self.has_header_row: bool = has_header_row
        self.column_widths: list[float] | None = column_widths
        self.text_alignment: list[TextAlignment] | None = text_alignment

    def __repr__(self):
        return f"Table({self.rows=}, {self.has_header_row=}, {self.column_widths=})"

    @classmethod
    def text_to_cell(cls, content: str) -> Cell:
        """Given some text, AST it and return a valid cell"""
        markdown = utils.create_markdown_it()
        ast = markdown.parse(content)

        current_run: CurrentRun = CurrentRun()
        current_row_entries: list[Entry] = []
        flat = utils.flatten_ast(ast)
        for token in utils.flatten_ast(ast):
            match token.type:
                # TODO Support underline and highlighting
                case "strong_open":
                    current_run.bold = True
                case "em_open":
                    current_run.italic = True
                case "text":
                    if token.content != "":
                        # Toss the empties, they shouldn't
                        # matter to end docx anyway
                        current_row_entries.append(
                            Entry(text=token.content, style=current_run)
                        )
                        # So they don't clutter each other
                        current_run = CurrentRun()

        return Cell(content=current_row_entries)

    @classmethod
    def from_csv_file(
        cls,
        file: Path,
        *,
        file_contains_headers: bool = True,
        column_widths: list[float] = None,
    ) -> Table:
        """Given a CSV file, turn it into a valid table

        Parameters
        ----------
        file: Path
            The file to read into a table
        file_contains_headers: bool
            Does the CSV contain a header row?

            Defaults to yes, but if not set then
            Pike will handle the relevant markdown shenanigans
        column_widths: list[float]
            A list of table column widths
        """
        rows: list[Row] = []
        if not file_contains_headers:
            rows.append(Row(cells=[]))

        with open(file) as f:
            reader = csv.reader(f)
            for row in reader:
                cells: list[Cell] = []
                for cell in row:
                    cells.append(cls.text_to_cell(cell))
                rows.append(Row(cells=cells))

        return cls(
            rows,
            has_header_row=file_contains_headers,
            column_widths=column_widths,
        )

    @classmethod
    def from_ast(
        cls,
        tokens: list[Token],
        table_context: TableContext = TableContext(),
    ) -> Table:
        """Given a Markdown table in AST format, retrieve a table"""
        text_alignment: list[TextAlignment] = []

        rows: list[Row] = []
        current_cells: list[Cell] = []
        current_row_entries: list[Entry] = []
        current_style: CurrentRun = CurrentRun()
        for token in utils.flatten_ast(tokens):
            if token.type == "th_open" and token.attrs.get("style"):
                # Get alignments
                match token.attrs["style"]:
                    case "text-align:right":
                        text_alignment.append(TextAlignment.RIGHT)
                    case "text-align:left":
                        text_alignment.append(TextAlignment.LEFT)
                    case "text-align:center":
                        text_alignment.append(TextAlignment.CENTER)

            match token.type:
                # TODO Support underline and highlighting
                case "strong_open":
                    current_style.bold = True
                case "strong_close":
                    current_style.bold = False
                case "em_open":
                    current_style.italic = True
                case "em_close":
                    current_style.italic = False
                case "text":
                    current_row_entries.append(
                        Entry(text=token.content, style=current_style)
                    )
                case "tr_close":
                    # We've finished a row
                    rows.append(Row(cells=current_cells))
                    current_cells = []
                case "th_close":
                    # Finished a cell in the header row
                    current_cells.append(Cell(content=current_row_entries))
                    current_row_entries = []
                case "td_close":
                    # Finished a data cell
                    current_cells.append(Cell(content=current_row_entries))
                    current_row_entries = []

        return cls(
            rows=rows,
            has_header_row=table_context.has_header_row,
            column_widths=table_context.column_widths,
            text_alignment=text_alignment,
        )
