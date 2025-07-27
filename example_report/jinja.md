---
id: jinja
description: TODO This needs completing
list:
  - 1
  - TODO well actually lists work fine now
---
The Jinja functions Pike exposes. 

You need to review the file `jinja.md` in order to view how these work functionally.

Insert an internal hyperlink to a bookmark:
{{insert_internal_hyperlink("MyFirstBookmark", "Click **ME** to go to the bookmark")}}

Raise a comment for review without it ending up in the final document:
{{comment("This is a comment")}}

Include an image using an easier syntax:
{{insert_image("images/cat.jpg", width=8.5, height=10, alt_text="Alt text", caption="Caption")}}

Insert a table from a csv:
{{insert_table_from_csv("data.csv")}}

Insert a page break in the current location:
{{add_page_break()}}

Insert a file as code:
{{this.plugins.insert_file_as_code("main.py")}}

Insert a table of contents:
{{insert_table_of_contents()}}

Insert a bookmark:
{{insert_bookmark("MyFirstBookmark", "Hello I am a bookmark that's **bold** and *italic*")}}

Bookmarks can also not have associated text:
{{insert_bookmark("MySecondBookmark")}}

Custom commands also work in tables:
| Header      |
| ----------- |
| {{insert_text("Hi I am ")}} {{insert_text("italic + bold", bold=True, italic=True)}} {{insert_text("and")}} {{insert_text("inline", inline=True)}}      |

{{insert_soft_break()}}
That's a soft break before this text. Useful for extra formatting and text after tables.