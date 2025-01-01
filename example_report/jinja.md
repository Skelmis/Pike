---
id: jinja
---
The Jinja functions Pike exposes. 

You need to review the file `jinja.md` in order to view how these work functionally.


Raise a comment for review without it ending up in the final document:
{{comment("This is a comment")}}

Include an image using an easier syntax:
{{insert_image("images/cat.jpg", width=8.5, height=10, alt_text="Alt text", caption="Caption")}}

Insert a page break in the current location:
{{add_page_break()}}