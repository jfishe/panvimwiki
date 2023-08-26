#!/usr/bin/env python3
r"""Remove * bullet list items from unordered list.

Plain text prefilter

- ``delete_bullet_star``: Remove unordered lists which use the star (asterisk)
  bullet marker. The pre-filter does not remove task list items (see
  `|delete_task_pending|`).
- Read stdin.
- Remove non-task * bullet lines, e.g., * [[URI|Description]] or * Text.
- Write filtered result to stdout.

.. code:: bash

    echo <<EOF | delete_bullet_star
    '- Bulleted list item 1 should appear'
    '* Bulleted list item 6 should NOT appear'
    EOF

.. code:: markdown

    - Bulleted list item 1 should appear

"""

from panvimwiki.filter.prefilter import prefilter

DELETE = r"^\s{0,}\*\s((?!\[\S\]\s).)*$"
REPLACE = None


def main():
    """Filter stdio with action()."""
    prefilter(delete=DELETE, replace=REPLACE)


if __name__ == "__main__":
    main()
