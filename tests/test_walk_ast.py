from docx import Document

from pike import Engine, File, utils
from pike.docx import Docx


def test_nested_blockquote(engine: Engine, data_dir) -> None:
    docx = Docx(engine)
    markdown = utils.create_markdown_it()
    ast = markdown.parse((data_dir / "nested_blockquote.md").read_text())
    docx.walk_ast(Document(), ast)
