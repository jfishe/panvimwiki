#!/usr/bin/env python3
"""Remove * bullet list items from unordered list.

Plain text filter
"""

import re
from typing import Tuple
from vimwiki_docx.filter.prefilter import prefilter


def action(line: str):
    r"""Regex to remove matching lines from Vimwiki entries.

        - Non-task * bullet lines, e.g., * [[URI|Description]] or * Text

    Parameters
    ----------
    line : Text to filter

    Returns
    -------
    Line that does not match the filter  r"^\s{0,}\*\s((?!\[\S\]\s).)*$",

    """
    regex: Tuple[str, ...] = (
        # Regex bullet *
        r"^\s{0,}\*\s((?!\[\S\]\s).)*$",
    )

    pattern = re.compile(r"|".join(regex))

    if re.search(pattern, line) is None:
        return line
    return None


def main():
    """Filter stdio with action()."""
    prefilter(action)

if __name__ == "__main__":
    main()
