Design ideals
-------------

This aims to be a simplistic markdown to word generator.

Variables are implemented using Jinja, with the syntax here: https://jinja.palletsprojects.com/en/3.1.x/templates/

Syntax overall is markdown.

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
7. Write the layout file to disk as markdown

Jinja tips
==========

- When defining a block, finish it with ``-%}`` instead of ``%}`` to ensure it doesn't appear as a newline within the document.