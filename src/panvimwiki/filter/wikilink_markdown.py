#!/usr/bin/env python3
r"""
Convert GitHub Flavored Markdown (gfm) to Vimwiki/Taskwiki syntax.

- Remove backslashes from [ ] tasks
- Remove backslashes from apostrophe-s, \`s.
- Remove link title "wikilink".
- Unescape taskwiki octothorpe and use asterisk-marker.

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
    # Unescape taskwiki octothorpe and use asterisk-marker.
    dict(
        pattern=r"(^\s{0,})-(\s\[.*)\\(#[0-9A-Fa-f]{8})$",
        repl=r"\1*\2\3",
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
