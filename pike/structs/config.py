from pydantic import BaseModel


class ListT(BaseModel):
    level_1: str
    level_2: str
    level_3: str


class StylesT(BaseModel):
    text: str = "Normal"
    """The text style to apply"""
    ordered_lists: ListT = ListT(
        level_1="List Paragraph", level_2="List Paragraph 2", level_3="List Paragraph 3"
    )
    """The style to apply for ordered lists"""
    bullet_lists: ListT = ListT(
        level_1="List Bullet", level_2="List Bullet 2", level_3="List Bullet 3"
    )
    """The style to apply for bullet (unordered) lists"""
    inline_code: str = ""
    """The style to use for inline code blocks"""
    code_block: str = ""
    """The style to use for code blocks"""
    table: str = "Table Grid"
    """The style to use for tables"""


class OutputDocumentsT(BaseModel):
    """Regardless of the combinations picked,
    Pike will still output the selected options."""

    markdown: bool = True
    """Output a markdown document"""
    docx: bool = True
    """Output a docx document"""
    pdf: bool = True
    """Output a pdf document"""


class CreationTypesT(BaseModel):
    """Word styles to create"""

    ordered_lists: bool = True
    """Should Pike create and use a default ordered list"""
    code_block: bool = True
    """Should Pike create and use a default code block"""
    inline_code: bool = True
    """Should Pike create and use a default inline code block"""


class ConfigT(BaseModel):
    layout_file: str | None = "layout.md"
    """The file to use as a template
    when generating the resultant report
    """
    configuration_directory: str = "configuration"
    """The directory containing configuration files"""
    docx_template: str | None = None
    """The docx file to use as a base template"""
    output_document_name: str = "report"
    """The name of the output file without an extension.
    Supports using variables from variables.json
    """
    output_directory: str = "documents"
    """The directory to create documents within.
    Must be a subdirectory of the parent report directory.
    """
    styles: StylesT = StylesT()
    """Styles to use in the word document"""
    output_files: OutputDocumentsT = OutputDocumentsT()
    """The resultant files to generate"""
    use_sandbox: bool = True
    """Whether or not to use a sandboxed Jinja2 environment"""
    docx_create_styles: CreationTypesT = CreationTypesT()
    """Should Pike create default styles?"""
    insert_at_last_paragraph: bool = False
    """Useful for inserting text after a given paragraph.
    
    Not enabled by default as it breaks items that don't deal 
    with text such as inserting images which"""
