"""Main function shared by prefilters."""

import re
import fileinput
from typing import Tuple


def action(line: str, delete: str = None, replace: Tuple[str, str] = None):
    """Filter Vimwiki text by deleting lines or replacing text in lines.

    Parameters
    ----------
    line : Line from Vimwiki file.

    delete : Regex string matching all or part of line to be deleted.

    replace : Regex re.search string and replacement string for re.sub.

    Returns
    -------
    Convert lines matching replace[0] regex by substituting replace[1].
    Lines that do not match delete regex.
    Otherwise return the original line. Replace takes precedes delete.

    """
    if replace is not None:
        re_search = re.compile(replace[0], re.MULTILINE)
        subst = replace[1]

        if re.search(re_search, line) is not None:
            return re.sub(re_search, subst, line, count=1)

    if delete is not None:
        re_delete = re.compile(delete, re.MULTILINE)

        if re.search(re_delete, line) is None:
            return line
        return None

    return line


def prefilter(delete: str = None, replace: Tuple[str, str] = None) -> None:
    """Read stdin, filter with action() to stdout.

    Parameters
    ----------
    delete : Regex string matching all or part of line to be deleted.

    replace : Regex re.search string and replacement string for re.sub.

    """
    for line in fileinput.input():
        lineout = action(line, delete, replace)
        if lineout is not None:
            print(lineout.rstrip("\n"))
