---
id: two
value: three
---
## Title {{ this.id }}

Content for file {{ this.id }}

{% set references = plugins.get_referenced_files() -%}
{% for reference in references -%}
This file is referenced by **{{ reference.id }}**
{% endfor -%}
