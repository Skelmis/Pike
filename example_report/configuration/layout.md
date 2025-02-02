{{ files.title_page.content }}

{% for file in get_folder('content') -%}
{{ file.content }}
{% endfor -%}

{{files.testing.content}}

Thanks for coming!

{{add_page_break()}}

{{ files.jinja.content }}

{{add_page_break()}}

{{ files.markdown.content }}