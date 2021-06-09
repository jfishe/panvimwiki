#!/usr/bin/env python3
"""Return the input with no changes.

Plain text filter
"""

from vimwiki_docx.filter.prefilter import prefilter


DELETE = None
REPLACE = None


def main():
    """Filter stdio with action()."""
    prefilter(delete=DELETE, replace=REPLACE)


if __name__ == "__main__":
    main()
