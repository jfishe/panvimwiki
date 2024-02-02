#!/usr/bin/env python3
"""
Convert pandoc markdown tasks and wikilinks.

Use Vimwiki markdown tasks and links. Remove "wikilink" link-title.

Plain text prefilter or post filter
"""

from __future__ import annotations

import re
import sys

DELETE = None
REPLACE = (
    # Remove backslashes from [ ] tasks.
    dict(
        pattern=r"\\\[(\S|\s)\\\]",
        repl=r"[\1]",
    ),
    # Remove backslashes from apostrophe-s, `s.
    dict(
        pattern=r"\\'s",
        repl=r"'s",
    ),
    # Remove link title "wikilink".
    dict(
        pattern=r" \"wikilink\"\)",
        repl=r")",
    ),
)


def main():
    """Filter stdio with action()."""
    lines = sys.stdin.read()
    for subst in REPLACE:
        lines = re.sub(**subst, string=lines, flags=re.MULTILINE)
    print(lines.rstrip("\n"))


if __name__ == "__main__":
    main()
