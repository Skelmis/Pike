from markdown_it import MarkdownIt
from markdown_it.token import Token


def create_markdown_it() -> MarkdownIt:
    markdown = MarkdownIt().enable("table")
    markdown.options["html"] = True
    return markdown


def flatten_ast(tokens: list[Token]) -> list[Token]:
    """Given a list of tokens, flatten it"""
    return [
        child if token.type == "inline" else token
        for token in tokens
        for child in (token.children if token.type == "inline" else [token])
    ]
