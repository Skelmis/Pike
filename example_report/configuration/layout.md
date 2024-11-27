{{ files.title_page.content }}

{% for file in get_folder('content') -%}
{{ file.content }}
{% endfor -%}

Thanks for coming!

PAGEBREAKSOMEHOW

{{ files.markdown.content }}