Using Pike
----------

There are two main ways to use Pike.

.. py:currentmodule:: pike.__main__

Command line usage
==================

You can use Pike from the command line.

Creating a new report
*********************

The following command will scaffold a directory into
the relevant structure for Pike to run against.

.. code-block:: shell

  python -m pike scaffold new_report

.. autofunction:: scaffold


Generating a report
*******************

The following will generate the report in the current directory.

.. code-block:: shell

  python -m pike run .

.. autofunction:: run


With a Python file
==================

This is useful when you want to extend Pike.

Create a file within your report directory like the following:

.. code-block:: python

  from pathlib import Path

  from pike import Engine


  def main():
      engine = Engine(Path("."))
      engine.run()


  if __name__ == "__main__":
      main()


An example way to use this to extend functionality is as follows:

.. code-block:: python

  from pathlib import Path

  from pike import Engine, File


  def get_referenced_files(file: File) -> list[File]:
      """Get all files that reference the current one."""
      data: list[File] = []
      for f in file.engine.files:
          if f == file:
              continue

          references = f.variables.get("references")
          if references is not None:
              if file.id in references:
                  data.append(f)

      return data


  def main():
      engine = Engine(Path("."))
      engine.register_file_plugin("get_referenced_files", get_referenced_files)
      engine.run()


  if __name__ == "__main__":
      main()


Running custom code within the context of Pike
==============================================

Simply running Python code
**************************

Pike provides a way to latch onto the runtime loop and run arbitrary Python
code in the context of the running report. This is useful for implementing
things such as helpful logging messages or enforcing xyz.

These are called injections, for example use cases please refer to the folder ``pike.injections``.

Exposing Python code within Jinja
*********************************

Sometimes instead of simply emitting some form of log message you may to expose
custom functionality within the Jinja template itself. This can be achieved
through Pike's plugin system and is demonstrated below.

.. code-block:: python

  from pathlib import Path

  from pike import Engine, File


  def get_referenced_files(file: File) -> list[File]:
      """Get all files that reference the current one."""
      data: list[File] = []
      for f in file.engine.files:
          if f == file:
              continue

          references = f.variables.get("references")
          if references is not None:
              if file.id in references:
                  data.append(f)

      return data


  def main():
      engine = Engine.load_from_directory(Path("."))
      engine.register_file_plugin("get_referenced_files", get_referenced_files)
      engine.run()


  if __name__ == "__main__":
      main()

While running this report, all file objects will now contain a plugin
called ``get_referenced_files`` which can be used like so:

.. code-block:: markdown

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

Jinja tips
==========

- When defining a block, finish it with ``-%}`` instead of ``%}`` to ensure it doesn't appear as a newline within the document.