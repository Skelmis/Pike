from __future__ import annotations

from enum import Enum
from typing import Literal

from markdown_it.token import Token


class EnumBase(Enum):
    def get_next(self) -> EnumBase:
        return type(self)(self.value + 1)

    def get_previous(self) -> EnumBase:
        return type(self)(self.value - 1)


class CurrentRun:
    """Defines various presentation metadata for runs"""

    def __init__(
        self,
        *,
        bold: bool = None,
        italic: bool = None,
        underline: bool = None,
        highlight: bool = None,
    ):
        # We use None to imply that Docx
        # should inherit any parent styling
        self.bold: bool | None = bold
        self.italic: bool | None = italic
        self.underline: bool | None = underline
        self.highlighted: bool | None = highlight

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __repr__(self):
        return f"CurrentRun({self.bold=},{self.italic=},{self.underline=},{self.highlighted=})"


class CurrentListNesting(EnumBase):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    # Maybe support more than 3 nested in future?
    # But I don't think that's too common of a requirement


class List:
    def __init__(
        self,
        list_type: Literal["ordered", "bullet"],
        nesting: CurrentListNesting,
    ):
        self.list_type = list_type
        self.nesting = nesting

    def __repr__(self):
        return f"List({self.list_type=}, {self.nesting=})"

    def __eq__(self, other):
        return (
            isinstance(other, List)
            and self.list_type == other.list_type
            and self.nesting == other.nesting
        )


class TableContext:
    """Context about the next table"""

    def __init__(
        self, *, column_widths: list[float] = None, has_header_row: bool = True
    ):
        self.column_widths = column_widths
        self.has_header_row = has_header_row


class Variables:
    """Top level container for variable state"""

    def __init__(self):
        self.current_run: CurrentRun = CurrentRun()
        # We use a list to support nested lists of different types
        self.current_lists: list[List] = []
        self._current_nesting: CurrentListNesting = CurrentListNesting.LEVEL_1
        self.next_table_context: TableContext = TableContext()

    def __repr__(self):
        return f"Variables({self.current_run=}, {self._current_nesting=}, {self.next_table_context=}, {self.current_lists=})"

    def get_current_list(self) -> List | None:
        if len(self.current_lists) == 0:
            return None

        return self.current_lists[-1]

    def add_nesting(self) -> None:
        if len(self.current_lists) == 0:
            # Only increment the nesting if we actually
            # have had a list entry instead of just anytime
            #
            # We do this as the AST walker will only
            # reset to LEVEL_1 and every new list
            # attempts to increment it, so we'd start
            # at LEVEL_2 for all lists otherwise
            return

        self._current_nesting = self._current_nesting.get_next()

    def remove_nesting(self) -> None:
        if self._current_nesting == CurrentListNesting.LEVEL_1:
            # Don't go lower than the lowest nesting
            return

        self._current_nesting = self._current_nesting.get_previous()

    def add_list(
        self,
        list_type: Literal["ordered", "bullet"],
        nesting: CurrentListNesting = None,
    ):
        if nesting is None:
            nesting = self._current_nesting
        self.current_lists.append(List(list_type, nesting))

    def remove_current_list(self) -> None:
        """Remove the current level of list"""
        if len(self.current_lists) == 0:
            return
        self.current_lists.pop()
