from markdown_it import MarkdownIt


def test_to_ast():
    markdown = MarkdownIt().enable("table")
    markdown.options["html"] = True
    ast = markdown.parse("# Heading")
    r_1 = ast[0]
    assert r_1.type == "heading_open"
