#!/usr/bin/env python3
"""Remove empty headings from Vimwiki file.

Headings are not empty if they contain tag lines. Execute `delete_tag_lines.py`
first to empty such headings.

Pandoc filter using panflute
"""

import panflute as pf


def prepare(doc):
    """Pre-filter."""


def action(elem, doc):
    """Remove empty headings from Vimwiki file."""
    if isinstance(elem, pf.Header):
        lookahead = elem.next
        if lookahead is None:
            return []
        if isinstance(lookahead, pf.Header) and lookahead.level <= elem.level:
            return []
    # return None -> element unchanged
    # return [] -> delete element
    return None


def finalize(doc):
    """Post-filter."""


def main(doc=None):
    """Remove empty headings from Vimwiki file.

    Pandoc filter using panflute
    """
    newdoc = pf.load()
    for i in range(5):
        newdoc = pf.run_filter(action, prepare=prepare, finalize=finalize, doc=newdoc)

    return pf.dump(newdoc)


if __name__ == "__main__":
    main()
