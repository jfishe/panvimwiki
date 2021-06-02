"""Main function shared by prefilters."""

import fileinput

def prefilter(action) -> None:
    """Read stdin, filter with action() to stdout.

    Parameters
    ----------
    action : Callable accepting line from stdin and returning line or None for
             stdout.

    """
    for line in fileinput.input():
        lineout = action(line)
        if lineout is not None:
            print(lineout.rstrip("\n"))
