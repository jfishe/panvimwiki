#!/usr/bin/env python3
"""Remove empty headings from Vimwiki file.

Headings are not empty if they contain tag lines. Execute `delete_tag_lines.py`
first to empty such headings.

Pandoc filter using panflute
"""

import panflute as pf


def prepare(doc):
    """Pre-filter."""
    pass


def action(elem, doc):
    """Remove empty headings from Vimwiki file."""
    if isinstance(elem. pf.ListItem):
        elem.walk(start2done1)
    if isinstance(elem, pf.BulletList) or isinstance(elem, pf.OrderedList):
        # pf.debug(elem)
        elem.replace_keyword("[S]", pf.Span(classes=["done1"]))
        elem.replace_keyword("[-]", pf.Span(classes=["doneX"]))
        return elem
    return None
    # return None -> element unchanged
    # return [] -> delete element


def start2done1(elem, doc):
    """TODO: Docstring for start2done1.

    Parameters
    ----------
    elem : TODO
    doc : TODO

    Returns
    -------
    TODO

    """
    if isinstance(elem, pf.Span) and 'done0' in elem.classes:
        pf.debug(elem.ancestor(2))
        elem.container.clear()
        pf.debug(elem.ancestor(2))
        return []


def finalize(doc):
    """Post-filter."""
    pass


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
