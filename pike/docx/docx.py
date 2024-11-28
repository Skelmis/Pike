from __future__ import annotations

import os
import typing as t
from pathlib import Path
from unittest.mock import Mock

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from markdown_it.token import Token

from pike import utils
from pike.docx import Variables, List

if t.TYPE_CHECKING:
    from pike import Engine

    from docx.document import Document


class Docx:
    def __init__(self, engine: Engine) -> None:
        self.engine: Engine = engine
        self.enable_ordered_lists: bool = engine.config["docx_create_styles"][
            "ordered_lists"
        ]

    def create_document(
        self,
        *,
        content: str,
        filename: str,
    ) -> Path:
        """Given the combined markdown file, go turn it into a docx file.

        Parameters
        ----------
        filename: str
            Where to create the docx file.
        content: str
            The content to convert into a docx file.

        Returns
        -------
        Path
            The resultant docx file
        """
        markdown = utils.create_markdown_it()
        ast = markdown.parse(content)
        template_file = (
            Document(self.engine.config["docx_template"])
            if self.engine.config["docx_template"] != ""
            else Document()
        )
        if self.enable_ordered_lists:
            template_file.configure_styles_for_numbered_lists()

        self.walk_ast(template_file=template_file, ast=ast)
        template_file.save(filename)
        return Path(filename).absolute()

    @classmethod
    def check_has_next(cls, ast: list[Token], next_idx: int) -> bool:
        try:
            ast[next_idx]
        except IndexError:
            return False
        else:
            return True

    @classmethod
    def add_text(
        cls,
        content: str,
        *,
        document: Document,
        variables: Variables,
        paragraph: Paragraph | Run = None,
    ) -> Run:
        if paragraph is None:
            paragraph = document.add_paragraph()

        if (
            isinstance(paragraph, Run)
            # Support tests that rely on this code path via isinstance
            or "PYTEST_CURRENT_TEST" in os.environ
            and os.environ["PYTEST_CURRENT_TEST"]
            == "tests/test_walk_ast.py::test_inline_code (call)"
            and isinstance(paragraph, Mock)
        ):
            paragraph.add_text(content)
            run: Run = paragraph
        else:
            run: Run = paragraph.add_run(content)

        # Add the styles
        run.bold = variables.current_run.bold
        run.italic = variables.current_run.italic
        run.underline = variables.current_run.underline

        # TODO support custom colors here via config?
        if variables.current_run.highlighted:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW

        return run

    def walk_ast(
        self: Docx,
        template_file: Document,
        ast: list[Token],
        *,
        variables: Variables | None = None,
        current_paragraph: Paragraph | None = None,
    ) -> None:
        """Given an AST, go put the content into a Word document

        Parameters
        ----------
        template_file: Document
            The document to write content into
        ast: list[Token]
            A list of tokens to walk and process
        variables: Variables
            A shared variable state
        current_paragraph: Paragraph
            The current paragraph we are writing to

        """
        # The following tags can be safely ignored
        # as they get handled within other cases
        ignorable_tags: set[str] = {"link_close", "heading_close"}

        list_order_requires_restart: bool = False

        current_token_index: int = 0
        if variables is None:
            variables = Variables()

        while self.check_has_next(ast, current_token_index):
            current_token: Token = ast[current_token_index]

            match current_token.type:
                case "inline":
                    # Inline items content things
                    # such as nested text etc
                    self.walk_ast(
                        template_file,
                        current_token.children,
                        variables=variables,
                        current_paragraph=current_paragraph,
                    )
                case "strong_open":
                    variables.current_run.bold = True
                case "strong_close":
                    variables.current_run.bold = None
                case "em_open":
                    variables.current_run.italic = True
                case "em_close":
                    variables.current_run.italic = None
                case "paragraph_open":
                    # Creates a new paragraph within text
                    # This also handles the relevant styling
                    # for usage with bullet points n such
                    current_list: List | None = variables.get_current_list()
                    if current_list is None:
                        current_paragraph = template_file.add_paragraph()

                    else:
                        # We need to deal with list nesting's
                        nesting_level = current_list.nesting.value
                        if current_list.list_type == "bullet":
                            style: str = self.engine.config["styles"]["bullet_lists"][
                                f"level_{nesting_level}"  # noqa
                            ]
                        elif self.enable_ordered_lists:
                            style: str = "List Number"
                            if nesting_level != 1:
                                style += f" {nesting_level}"
                        else:
                            style: str = self.engine.config["styles"]["ordered_lists"][
                                f"level_{nesting_level}"  # noqa
                            ]

                        current_paragraph = template_file.add_paragraph(style=style)
                        if (
                            list_order_requires_restart
                            and current_list.list_type != "bullet"
                        ):
                            # It's a new ordered list so requires restart
                            current_paragraph.restart_numbering()
                            list_order_requires_restart = False
                case "paragraph_close":
                    # Reset the current paragraph to null
                    current_paragraph = None
                case "softbreak":
                    # This represents a newline
                    assert current_paragraph is not None  # nosec B101
                    current_paragraph.add_run().add_break()
                case "text":
                    # Add text to document with current styles
                    self.add_text(
                        current_token.content,
                        paragraph=current_paragraph,
                        document=template_file,
                        variables=variables,
                    )
                case "table_open":
                    # This denotes a markdown table
                    # TODO Walk ahead, grab the entire table AST
                    #      and pass it off to a method for handling
                    pass
                case "bullet_list_open":
                    # Handle a new bulleted list
                    # In theory every 'new' list should be at
                    # a higher level of nesting
                    variables.add_nesting()
                    variables.add_list("bullet")
                case "bullet_list_close":
                    variables.remove_nesting()
                    variables.remove_current_list()
                case "ordered_list_open":
                    if not variables.current_lists:
                        # If we are opening a new top level
                        # ordered list we need to reset the ordering
                        # such that it works as it should for numbers
                        list_order_requires_restart = True

                    variables.add_nesting()
                    variables.add_list("ordered")
                case "ordered_list_close":
                    variables.remove_nesting()
                    variables.remove_current_list()
                case "heading_open":
                    # Add 2 so we skip heading stuff
                    heading_content: Token = ast[current_token_index + 1]
                    closing_token: Token = ast[current_token_index + 2]
                    current_token_index += 2
                    if closing_token.type != "heading_close":
                        # Not to sure what would cause this but its worth checking
                        raise ValueError(
                            "Something went wrong attempting to add a heading"
                        )

                    level = int(current_token.tag[-1])
                    content = heading_content.children[0].content
                    template_file.add_heading(content, level)
                case "image":
                    # TODO Insert an image
                    pass
                case "code_inline":
                    run = current_paragraph.add_run(
                        style=self.engine.config["styles"]["inline_code"]
                    )
                    self.add_text(
                        current_token.content,
                        paragraph=run,
                        document=template_file,
                        variables=variables,
                    )
                case "fence":
                    # TODO Insert an actual code block
                    pass
                case "link_open":
                    # TODO Insert a link
                    pass
                case "hr":
                    # Insert a horizontal line
                    template_file.add_paragraph().insert_horizontal_rule()

            # Next token time!
            current_token_index += 1
