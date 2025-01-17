.. _Custom Commands:

Custom Command Syntax
=====================

Pike supports the ability for custom commands to be
embedded within Markdown documents with which the AST
will then pick up and run. This essentially lets users
provide custom functionality on top of what raw
Markdown has to offer.

Sometimes the AST will fail to parse out a command from
text / other items. If this happens please open an issue.

I've considered making it a smart check on text, but
until I can reproduce said things I find it unlikely.

Command Syntax
--------------

In order to ensure these commands end up in the AST
Pike use's HTML blocks which are then parsed out into syntax.

The format is as follows:

.. code-block:: text

  <MARKER NAME ARGS [...]KWARGS [...]>

In this we have the following:
- ``MARKER``: This represents a prefix for Pike to check to ensure we are actually dealing with a custom command and not a regular HTML block. This is an MD5 Hash
- ``NAME`` represents the name of the custom command to be called
- ``ARGS`` represents positional arguments to supply to the command
- ``KWARGS`` represents keyword arguments to supply to the command

Both ``ARGS`` and ``KWARGS`` values are also base64 encoded to easier allow for a wider range of input data.

An example of this in action may look like:

.. code-block:: text

  <MARKER insert_code_block_from_file ARGS KWARGS file_path|(BASE64->)./code.py>
  <MARKER insert_code_block_from_file ARGS KWARGS file_path|Li9jb2RlLnB5>

.. py:currentmodule:: pike.docx.commands

.. autoclass:: Command
  :members:
  :undoc-members:

.. autofunction:: parse_command_string

.. autofunction:: create_command_string

.. py:attribute:: MARKER