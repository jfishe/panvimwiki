#!/usr/bin/env python3
"""Remove Pending and Waiting tasks and set Start tasks to [.]{.done1}.

Plain text filter
"""

import re

from vimwiki_docx.filter.prefilter import prefilter


def action(line: str):
    """Remove Pending and Waiting tasks and change Start to [.].

    Parameters
    ----------
    line : Line from Vimwiki file.

    Returns
    -------
    Lines that do not match Tasks Pending [ ] or Waiting [W].
    Convert Tasks Start [S] to [.].

    """
    re_not_start = re.compile(r"\s\[[\sW]\]", re.MULTILINE)
    re_start = re.compile(r"\s\[S\]", re.MULTILINE)
    subst = " [.]"

    if re.search(re_not_start, line) is not None:
        return None
    elif re.search(re_start, line) is not None:
        return re.sub(re_start, subst, line, count=1)
    else:
        return line


def main():
    """Filter stdio with action()."""
    prefilter(action)

if __name__ == "__main__":
    main()
