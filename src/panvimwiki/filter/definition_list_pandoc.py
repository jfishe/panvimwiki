#!/usr/bin/env python3
r"""Convert Vimwiki markdown definition lists to pandoc definition_lists.

Plain text prefilter

- Read stdin.
- Convert ``Term:: Definition`` to ``Term`` and ``: Definition``.
- Convert ``Term::`` to ``Term``.
- Convert ``:: Definition`` to ``: Definition``.
- Separate definition lists from adjacent paragraphs with an empty line.
- Skip fenced code blocks and pandoc fenced divs, ``:::``.
- Write filtered result to stdout.

Example
_______
.. code:: bash

    printf 'Term 1:: Definition 1\n\nTerm 2::\n:: Definition 2\n' |
    definition_list_pandoc

.. code:: none

    Term 1
    : Definition 1

    Term 2
    : Definition 2

"""

from __future__ import annotations

import re
import sys

TERM = re.compile(r"^(?![:\s])(?P<term>.*?)(?<!:)::(?:\s+(?P<definition>.*?))?\s*$")
"""Vimwiki term with optional definition, e.g., ``Term:: Definition``."""
DEFINITION = re.compile(r"^::\s+(?P<definition>.*?)\s*$")
"""Vimwiki definition without a term, e.g., ``:: Definition``."""
FENCE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})")
"""Opening or closing fence of a fenced code block."""


def definition_list_pandoc(lines: list[str]) -> list[str]:
    """Convert Vimwiki definition lists to pandoc definition_lists.

    Parameters
    ----------
    lines
        Vimwiki markdown lines without line endings.

    Returns
    -------
    list[str]
        Lines with pandoc definition_lists.

    """
    output: list[str] = []
    fence: str | None = None
    in_list = False

    def separate() -> None:
        if output and output[-1].strip():
            output.append("")

    for line in lines:
        if fence is not None:
            output.append(line)
            match = FENCE.match(line)
            if match is not None and match["fence"].startswith(fence):
                fence = None
            continue

        match = FENCE.match(line)
        if match is not None:
            fence = match["fence"]
            if in_list:
                separate()
                in_list = False
            output.append(line)
            continue

        if (match := DEFINITION.match(line)) is not None and in_list:
            output.append(": " + match["definition"])
        elif (match := TERM.match(line)) is not None:
            separate()
            output.append(match["term"].rstrip())
            if match["definition"]:
                output.append(": " + match["definition"])
            in_list = True
        else:
            if in_list and line.strip():
                separate()
            in_list = False
            output.append(line)

    return output


def main():
    """Filter stdio with definition_list_pandoc()."""
    lines = sys.stdin.read().splitlines()
    for line in definition_list_pandoc(lines):
        print(line)


if __name__ == "__main__":
    main()
