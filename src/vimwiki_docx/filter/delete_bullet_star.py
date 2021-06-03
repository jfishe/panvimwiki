#!/usr/bin/env python3
"""Remove * bullet list items from unordered list.

Plain text filter

- Read stdin.
- Remove non-task * bullet lines, e.g., * [[URI|Description]] or * Text.
- Write filtered result to stdout.
"""

from vimwiki_docx.filter.prefilter import prefilter


DELETE = r"^\s{0,}\*\s((?!\[\S\]\s).)*$"
REPLACE = None


def main():
    """Filter stdio with action()."""
    prefilter(delete=DELETE, replace=REPLACE)


if __name__ == "__main__":
    main()
