#!/usr/bin/env python3
"""Remove taskwiki heading.

Pandoc filter using panflute
"""

import re
import panflute as pf


def prepare(doc):
    """Pre-filter."""
    pass


def action(elem, doc):
    """Remove taskwiki heading."""
    regex = re.compile(r"\|.*$", re.MULTILINE)
    subst = ""

    if isinstance(elem, pf.Header):
        result = re.sub(regex, subst, elem.identifier, 0)
        elem.content = pf.convert_text(result)[0].content
        elem.identifier = result
        return elem
    # return None -> element unchanged
    # return [] -> delete element
    return None


def finalize(doc):
    """Post-filter."""
    pass


def main(doc=None):
    """Remove taskwiki heading.

    Pandoc filter using panflute
    """
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
