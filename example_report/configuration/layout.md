{{ files.title_page.content }}

{% for file in get_folder('content') -%}
{{ file.content }}
{% endfor -%}

Thanks for coming!

{{add_page_break()}}
{{ files.jinja.content }}
{{add_page_break()}}
{{ files.markdown.content }}