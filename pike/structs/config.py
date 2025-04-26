from typing import TypedDict


class ListT(TypedDict):
    level_1: str
    level_2: str
    level_3: str


class StylesT(TypedDict):
    text: str
    """The text style to apply"""
    ordered_lists: ListT
    """The style to apply for ordered lists"""
    bullet_lists: ListT
    """The style to apply for bullet (unordered) lists"""
    inline_code: str
    """The style to use for inline code blocks"""
    code_block: str
    """The style to use for code blocks"""
    table: str
    """The style to use for tables"""


class OutputDocumentsT(TypedDict):
    """Regardless of the combinations picked,
    Pike will still output the selected options."""

    markdown: bool
    """Output a markdown document"""
    docx: bool
    """Output a docx document"""
    pdf: bool
    """Output a pdf document"""


class CreationTypesT(TypedDict):
    """Word styles to create"""

    ordered_lists: bool
    """Should Pike create and use a default ordered list"""
    code_block: bool
    """Should Pike create and use a default code block"""
    inline_code: bool
    """Should Pike create and use a default inline code block"""


class ConfigT(TypedDict):
    layout_file: str | None
    """The file to use as a template
    when generating the resultant report
    """
    docx_template: str
    """The docx file to use as a base template"""
    output_document_name: str
    """The name of the output file without an extension.
    Supports using variables from variables.json
    """
    output_directory: str
    """The directory to create documents within.
    Must be a subdirectory of the parent report directory.
    """
    styles: StylesT
    """Styles to use in the word document"""
    output_files: OutputDocumentsT
    """The resultant files to generate"""
    use_sandbox: bool
    """Whether or not to use a sandboxed Jinja2 environment"""
    docx_create_styles: CreationTypesT
    """Should Pike create default styles?"""
