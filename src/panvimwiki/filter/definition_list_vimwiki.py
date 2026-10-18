#!/usr/bin/env python3
r"""Convert pandoc definition_lists to Vimwiki markdown definition lists.

Plain text post filter

- Read stdin.
- Convert ``Term`` and a single ``: Definition`` to ``Term:: Definition``.
- Convert ``Term`` and multiple ``: Definition`` lines to ``Term::`` followed
  by ``:: Definition`` lines.
- Skip fenced code blocks and definitions with continuation lines.
- Write filtered result to stdout.

Example
_______
.. code:: bash

    printf 'Term 1\n: Definition 1\n\nTerm 2\n: Definition 2\n: Definition 3\n' |
    definition_list_vimwiki

.. code:: none

    Term 1:: Definition 1

    Term 2::
    :: Definition 2
    :: Definition 3

"""

from __future__ import annotations

import re
import sys

from panvimwiki.filter.definition_list_pandoc import FENCE

DEFINITION = re.compile(r"^:\s+(?P<definition>\S.*?)\s*$")
"""Pandoc definition, e.g., ``: Definition``."""


def definition_list_vimwiki(lines: list[str]) -> list[str]:
    """Convert pandoc definition_lists to Vimwiki definition lists.

    Parameters
    ----------
    lines
        Pandoc markdown lines without line endings.

    Returns
    -------
    list[str]
        Lines with Vimwiki definition lists.

    """
    output: list[str] = []
    fence: str | None = None
    index = 0

    while index < len(lines):
        line = lines[index]

        if fence is not None:
            output.append(line)
            match = FENCE.match(line)
            if match is not None and match["fence"].startswith(fence):
                fence = None
            index += 1
            continue

        match = FENCE.match(line)
        if match is not None:
            fence = match["fence"]
            output.append(line)
            index += 1
            continue

        definitions: list[str] = []
        end = index + 1
        if line.strip() and not line.startswith((":", " ", "\t")):
            while (
                end < len(lines) and (match := DEFINITION.match(lines[end])) is not None
            ):
                definitions.append(match["definition"])
                end += 1

        # Leave definitions with continuation lines unchanged.
        if definitions and (end == len(lines) or not lines[end].strip()):
            if len(definitions) == 1:
                output.append(f"{line}:: {definitions[0]}")
            else:
                output.append(f"{line}::")
                output.extend(f":: {definition}" for definition in definitions)
            index = end
        else:
            output.append(line)
            index += 1

    return output


def main():
    """Filter stdio with definition_list_vimwiki()."""
    lines = sys.stdin.read().splitlines()
    for line in definition_list_vimwiki(lines):
        print(line)


if __name__ == "__main__":
    main()
