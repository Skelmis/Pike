Design ideals
-------------

Goals
=====

1. This aims to be a simplistic markdown to word/pdf generator
2. Variables are implemented using pre-existing solutions such as Jinja
3. This software should be fast. Users shouldn't wait unreasonable time for a report to generate

1
*
Users should be able to write simple markdown files which are transformed into beautiful word / PDF documents. User's should not need to care about formatting beyond markdown.

2
*
No reinventing the wheel. Variables and plugin hooks are done via Jinja. Specifically: https://jinja.palletsprojects.com/en/3.1.x/templates/

3
*
Pike should be fast. Ideally there shouldn't be enough downtime to do something else like go grab a coffee.

This will be archived by never touching Latex, and instead using word as an intermediary. This also provides more freedom to end users when they wish to create new templates.

*grumbles about existing solutions taking enough time to make a coffee*



Variable Namespace
==================

Files look like this
********************

Imagine the file ``one.md`` in folder ``content``

.. code-block:: markdown

  ---
  id: one
  value: two
  ---
  Content goes here

Which becomes the following lookup tree:

.. code-block:: json

  {
    "id": "one",
    "value": "two",
    "content": "Content goes here"
  }

This will be referred to using the string ``FV`` in later dicts.

Global variables
****************

Variables from ``variables.json`` get loaded in as JSON. For example:

.. code-block:: json

  {
    "project_id": "Test"
  }

Injection namespace
*******************

When injecting a file the namespace looks like this:

.. code-block:: json

  {
    "one": "FV",
    "files": {
      "one": "FV"
    },
    "folders": {
      "content": ["FV"]
    },
    "project_id": "Test",
    "globals": {
      "project_id": "Test"
    }
  }

We inject at both the global namespace and under specific keys to reduce the risk of overwriting specific keys etc.

TODO In future warn on duplicate keys

Runtime loop
============

1. Open all files and load frontmatter
2. Update global [lookup dict of variables](#injection-namespace)
3. Loop over all files injecting variables
4. Update global lookup dict again
5. Run all associated injections (By this point all files bar layout file should be filled)
6. Inject said all files into the layout file
7. Write the layout file to disk as markdown/word/pdf

