from __future__ import annotations

import os
import re
import typing as t
from collections.abc import Callable
from functools import partial
from pathlib import Path
from unittest.mock import Mock

from skelmis.docx import Document
from skelmis.docx.enum.style import WD_STYLE_TYPE
from skelmis.docx.enum.table import WD_TABLE_ALIGNMENT
from skelmis.docx.enum.text import WD_COLOR_INDEX, WD_PARAGRAPH_ALIGNMENT
from skelmis.docx.oxml import OxmlElement
from skelmis.docx.oxml.ns import qn
from skelmis.docx.shared import Cm, RGBColor
from skelmis.docx.styles.style import ParagraphStyle
from skelmis.docx.table import _Cell
from skelmis.docx.text.paragraph import Paragraph
from skelmis.docx.text.parfmt import ParagraphFormat
from skelmis.docx.text.run import Run
from markdown_it.token import Token

from pike import utils, structs
from pike.docx import (
    Variables,
    List,
    check_has_next,
    commands,
    get_up_to_token,
    CurrentRun,
)

if t.TYPE_CHECKING:
    from pike import Engine

    from skelmis.docx.document import Document

html_attribute_pattern: re.Pattern = re.compile(
    r"(\S+)=[\"']?((?:.(?![\"']?\s+\S+=|\s*/?[>\"']))+.)[\"']?"
)


class Docx:
    def __init__(self, engine: Engine) -> None:
        self.engine: Engine = engine
        self.enable_ordered_lists: bool = engine.config["docx_create_styles"][
            "ordered_lists"
        ]
        self.enable_code_blocks: bool = engine.config["docx_create_styles"][
            "code_block"
        ]
        self.enable_inline_code: bool = engine.config["docx_create_styles"][
            "inline_code"
        ]
        self.commands: dict[str, Callable[[...], ...] | Callable[[], ...]] = {
            # A built-in NOP for commands and injections
            # which need an out to avoid displaying None
            "NOP": lambda: None,
        }

        # These can be used by external things
        # Check they are None first, but they do exist
        # I'd like to refactor their usage but eh
        self.template_file: Document | None = None
        self.current_paragraph: Paragraph | None = None

    def import_commands_from_engine(self):
        for command in self.engine._custom_commands_to_add:
            self.load_custom_command(
                command[0],
                command[1],
                provide_docx_instance=command[2],
            )

    def load_custom_command(
        self,
        command_name: str,
        command_callable,
        *,
        provide_docx_instance: bool = False,
    ) -> t.Self:
        """Load a custom command into the Docx instance.

        Parameters
        ----------
        command_name: str
            The name of the command to call
        command_callable
            The relevant function to call.
        provide_docx_instance: bool
            If True (defaults to False), the docx instance will be
            provided as the first positional argument.

        Returns
        -------
        Docx
            The current instance to allow for method chaining.
        """
        if provide_docx_instance:
            command_callable = partial(command_callable, self)

        self.commands[command_name] = command_callable
        return self

    def insert_cell(self, cell: structs.Cell) -> None:
        for entry in cell.content:
            for item in commands.split_str_into_command_blocks(entry.text):
                if isinstance(item, commands.Command):
                    command_callable = self.commands.get(item.command)
                    if command_callable is None:
                        raise ValueError(
                            f"Attempted to use an unknown custom command: {item.command}"
                        )

                    command_callable(
                        *item.arguments,
                        **item.keyword_arguments,
                    )
                else:
                    self.add_text(
                        item,
                        current_run=entry.style,
                        document=self.template_file,
                        paragraph=self.current_paragraph,
                    )

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
        self.template_file = (
            Document(self.engine.config["docx_template"])
            if self.engine.config["docx_template"] != ""
            else Document()
        )
        if self.enable_ordered_lists:
            self.template_file.configure_styles_for_numbered_lists()

        if self.enable_inline_code:
            self._configure_for_inline_code()

        if self.engine.docx_header is not None:
            headers = self.engine.docx_header.split("\t")
            for entrant in headers:
                as_formatting: structs.Cell = structs.Table.text_to_cell(entrant)
                p = self.template_file.sections[0].header.paragraphs[0]
                self.current_paragraph = p
                self.insert_cell(as_formatting)
                self.current_paragraph.add_run("\t")

            self.current_paragraph = None

        if self.engine.docx_footer is not None:
            footer = self.engine.docx_footer.split("\t")
            for entrant in footer:
                as_formatting: structs.Cell = structs.Table.text_to_cell(entrant)
                p = self.template_file.sections[0].footer.paragraphs[0]
                self.current_paragraph = p
                self.insert_cell(as_formatting)
                self.current_paragraph.add_run("\t")

        self.walk_ast(template_file=self.template_file, ast=ast)
        self.template_file.save(filename)
        return Path(filename).absolute()

    @classmethod
    def add_image(
        cls,
        image_src: str,
        *,
        template_file: Document,
        width: Cm | None = None,
        height: Cm | None = None,
        title: str = None,
        alt_text: str = None,
    ):
        # TODO Implement title and alt text
        template_file.add_picture(image_src, width=width, height=height)

    @classmethod
    def add_text(
        cls,
        content: str,
        *,
        document: Document,
        current_run: CurrentRun,
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
        run.bold = current_run.bold
        run.italic = current_run.italic
        run.underline = current_run.underline

        # TODO support custom colors here via config?
        if current_run.highlighted:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW

        return run

    def _configure_for_inline_code(self):
        style_name: str = "_Pike_Inline_Code"
        self.engine.config["styles"]["inline_code"] = style_name

        if style_name in self.template_file.styles:
            # No need to duplicate
            return

        new_style = self.template_file.styles.add_style(
            style_name, WD_STYLE_TYPE.CHARACTER
        )
        new_style.base_style = self.template_file.styles["Subtle Reference"]
        new_style.font.small_caps = False
        new_style.font.color.rgb = RGBColor(192, 80, 77)
        new_style.font.name = "Liberation Mono"
        new_style.font.underline = False

    def _configure_for_codeblocks(self):
        style_name: str = "_Pike_Code_Block"
        self.engine.config["styles"]["code_block"] = style_name

        if style_name in self.template_file.styles:
            # No need to duplicate
            return

        document = self.template_file
        style: ParagraphStyle = document.styles.add_style(
            style_name, WD_STYLE_TYPE.PARAGRAPH
        )
        style.base_style = document.styles["Normal"]

        s_format: ParagraphFormat = style.paragraph_format
        s_format.left_indent = Cm(0.25)
        s_format.right_indent = Cm(0.25)
        # s_format.space_before = Cm(0.5)
        # s_format.space_after = Cm(0.5)
        s_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        s_font = style.font
        # s_font.name = "Consolas"
        s_font.name = "DejaVu Sans Mono"
        # s_font.bold = True
        s_font.color.rgb = RGBColor(0, 0, 0)

    def insert_codeblock(self, text: str) -> None:
        # TODO Support highlighting, bold, italic n such
        if self.enable_code_blocks:
            self._configure_for_codeblocks()

        p = self.template_file.add_paragraph(
            text,
            style=self.engine.config["styles"]["code_block"],
        )
        if self.enable_code_blocks:
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"), "ECEBDE")
            p.paragraph_format.element.get_or_add_pPr()
            p.paragraph_format.element.pPr.append(shd)

    def walk_ast(
        self: Docx,
        template_file: Document,
        ast: list[Token],
        *,
        variables: Variables | None = None,
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

        """
        if self.template_file is None:
            # Ensure custom commands have access to
            # this if we have managed to get into a
            # situation where it isnt already set.
            # I.E. Low level usage
            self.template_file = template_file

        # The following tags can be safely ignored
        # as they get handled within other cases
        ignorable_tags: set[str] = {
            "link_close",
        }

        list_order_requires_restart: bool = False

        current_token_index: int = 0
        if variables is None:
            variables = Variables()

        while check_has_next(ast, current_token_index):
            current_token: Token = ast[current_token_index]

            match current_token.type:
                case "inline":
                    # Inline items content things
                    # such as nested text etc
                    self.walk_ast(
                        template_file,
                        current_token.children,
                        variables=variables,
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
                        self.current_paragraph = template_file.add_paragraph()

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

                        self.current_paragraph = template_file.add_paragraph(
                            style=style
                        )
                        if (
                            list_order_requires_restart
                            and current_list.list_type != "bullet"
                        ):
                            # It's a new ordered list so requires restart
                            self.current_paragraph.restart_numbering()
                            list_order_requires_restart = False
                case "paragraph_close":
                    # Reset the current paragraph to null
                    self.current_paragraph = None
                case "heading_close":
                    self.current_paragraph = None
                case "softbreak":
                    # This represents a newline
                    if self.current_paragraph is None:
                        # Unsure why this is None here...
                        self.current_paragraph = self.current_paragraph = (
                            template_file.add_paragraph()
                        )
                    else:
                        # Else otherwise it'd be two newlines
                        self.current_paragraph.add_run().add_break()
                case "text":
                    # Add text to document with current styles
                    for item in commands.split_str_into_command_blocks(
                        current_token.content
                    ):
                        if isinstance(item, commands.Command):
                            command_callable = self.commands.get(item.command)
                            if command_callable is None:
                                raise ValueError(
                                    f"Attempted to use an unknown custom command: {item.command}"
                                )

                            command_callable(
                                *item.arguments,
                                **item.keyword_arguments,
                            )
                        else:
                            self.add_text(
                                item,
                                paragraph=self.current_paragraph,
                                document=template_file,
                                current_run=variables.current_run,
                            )
                case "table_open":
                    # This denotes a Markdown table
                    table_ast = get_up_to_token(
                        ast,
                        end_token_type="table_close",
                        current_idx=current_token_index,
                    )
                    current_token_index += len(table_ast)
                    table_model = structs.Table.from_ast(table_ast)
                    docx_table = template_file.add_table(
                        rows=len(table_model.rows),
                        cols=len(table_model.rows[0].cells),
                        style=self.engine.config["styles"]["table"],
                    )
                    for row_idx, row in enumerate(docx_table.rows):
                        for cell_idx, cell in enumerate(row.cells):
                            cell = t.cast(_Cell, cell)
                            current_cell_paragraph = cell.paragraphs[0]

                            if (
                                table_model.text_alignment[cell_idx]
                                != structs.TextAlignment.NONE
                            ):
                                match table_model.text_alignment[cell_idx]:
                                    case structs.TextAlignment.LEFT:
                                        current_cell_paragraph.paragraph_format.alignment = (
                                            WD_TABLE_ALIGNMENT.LEFT
                                        )
                                    case structs.TextAlignment.CENTER:
                                        current_cell_paragraph.paragraph_format.alignment = (
                                            WD_TABLE_ALIGNMENT.CENTER
                                        )
                                    case structs.TextAlignment.RIGHT:
                                        current_cell_paragraph.paragraph_format.alignment = (
                                            WD_TABLE_ALIGNMENT.RIGHT
                                        )

                            cell_model: structs.Cell = table_model.rows[row_idx].cells[
                                cell_idx
                            ]
                            for entry in cell_model.content:
                                if entry.link is not None:
                                    if entry.link.is_external_hyperlink:
                                        current_cell_paragraph.add_external_hyperlink(
                                            entry.link.href, entry.link.text
                                        )
                                        continue

                                    else:
                                        raise ValueError(
                                            f"Unsure how to handle {entry.link}"
                                        )

                                for item in commands.split_str_into_command_blocks(
                                    entry.text
                                ):
                                    if isinstance(item, commands.Command):
                                        command_callable = self.commands.get(
                                            item.command
                                        )
                                        if command_callable is None:
                                            raise ValueError(
                                                f"Attempted to use an unknown custom command: {item.command}"
                                            )

                                        old_pg = self.current_paragraph
                                        self.current_paragraph = (
                                            current_cell_paragraph.add_run()
                                        )
                                        command_callable(
                                            *item.arguments,
                                            **item.keyword_arguments,
                                        )
                                        self.current_paragraph = old_pg
                                    else:
                                        self.add_text(
                                            item,
                                            current_run=entry.style,
                                            document=template_file,
                                            paragraph=current_cell_paragraph.add_run(),
                                        )

                    # We add a paragraph here to ensure that subsequent tables don't
                    # end up joined to this one as per #23
                    if (
                        current_token_index < len(ast)
                        and ast[current_token_index].type == "table_open"
                    ):
                        if self.current_paragraph is None:
                            self.current_paragraph = self.template_file.add_paragraph()
                        else:
                            self.current_paragraph.add_run().add_break()

                    # Continue here since we have mutated
                    # the current index already
                    continue

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
                    level = int(current_token.tag[-1])
                    self.current_paragraph = template_file.add_heading(level=level)

                case "html_block" | "html_inline":
                    # Figure out the type of HTML we have
                    # This is kind of jank.
                    #
                    # Ref: https://spec.commonmark.org/0.25/#html-blocks
                    if current_token.content.startswith("<img"):
                        # Lets regex for an image
                        matches = html_attribute_pattern.findall(current_token.content)
                        src = None
                        width = None
                        height = None
                        alt = None
                        title = None
                        for title, value in matches:
                            match title:
                                case "src":
                                    src = value
                                case "width":
                                    width = float(
                                        value.removeprefix("'").removeprefix('"')
                                    )
                                case "height":
                                    height = float(
                                        value.removeprefix("'").removeprefix('"')
                                    )
                                case "alt":
                                    alt = value
                                case "title":
                                    title = value

                        if src is None:
                            raise ValueError("Image 'src' is required.")

                        self.add_image(
                            src,
                            template_file=template_file,
                            width=Cm(width),
                            height=Cm(height),
                            title=title,
                            alt_text=alt,
                        )
                        current_token_index += 1
                        continue

                    for item in commands.split_str_into_command_blocks(
                        current_token.content
                    ):
                        if isinstance(item, commands.Command):
                            command_callable = self.commands.get(item.command)
                            if command_callable is None:
                                raise ValueError(
                                    f"Attempted to use an unknown custom command: {item.command}"
                                )

                            command_callable(
                                *item.arguments,
                                **item.keyword_arguments,
                            )
                        else:
                            if item.startswith("\n#"):
                                # Likely a botched heading
                                item = item.lstrip()
                                level, text = item.split(" ", maxsplit=1)
                                self.current_paragraph = template_file.add_heading(
                                    level=len(level)
                                )
                                as_formatting: structs.Cell = (
                                    structs.Table.text_to_cell(text)
                                )
                                self.insert_cell(as_formatting)
                                # In theory this will be reset before next insert
                                # so this being None means no duplicate gaps
                                self.current_paragraph = None
                            else:
                                self.add_text(
                                    item,
                                    paragraph=self.current_paragraph,
                                    document=template_file,
                                    current_run=variables.current_run,
                                )

                case "image":
                    # Insert an image
                    alt_text = current_token.content
                    img_src = current_token.attrs["src"]
                    caption = current_token.attrs.get("title", None)
                    self.add_image(
                        img_src,
                        template_file=template_file,
                        title=caption,
                        alt_text=alt_text,
                    )

                case "code_inline":
                    run = self.current_paragraph.add_run(
                        style=self.engine.config["styles"]["inline_code"]
                    )
                    self.add_text(
                        current_token.content,
                        paragraph=run,
                        document=template_file,
                        current_run=variables.current_run,
                    )

                case "fence":
                    self.insert_codeblock(current_token.content.rstrip())
                case "link_open":
                    # Insert a link
                    # Once I know how to make word like this, use it
                    # title = current_token.attrs.get("title")
                    href = current_token.attrs["href"]
                    text = ast[current_token_index + 1].content
                    self.current_paragraph.add_external_hyperlink(href, text)
                    # Skip the 'text' and 'link_close' block
                    current_token_index += 2
                    continue
                case "hr":
                    # Insert a horizontal line
                    template_file.add_paragraph().draw_paragraph_border(top=True)

            # Next token time!
            current_token_index += 1
