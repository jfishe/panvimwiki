#!/usr/bin/env python3
"""Remove empty headings from Vimwiki file.

Pandoc filter using panflute
"""

import panflute as pf


def prepare(doc):
    """Pre-filter."""
    pass


def action(elem, doc):
    """Remove empty headings from Vimwiki file."""
    if type(elem) == pf.Header:
        lookahead = elem.next
        if lookahead is None:
            return []
        if type(lookahead) == pf.Header and lookahead.level <= elem.level:
            return []
    # return None -> element unchanged
    # return [] -> delete element
    return None


def finalize(doc):
    """Post-filter."""
    pass


def main(doc=None):
    """Remove empty headings from Vimwiki file.

    Pandoc filter using panflute
    """
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
