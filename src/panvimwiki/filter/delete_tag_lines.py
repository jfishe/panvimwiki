#!/usr/bin/env python3
"""Remove Vimwiki tag lines, e.g., :tag1:tag2:.

Pandoc filter using panflute
"""

import panflute as pf


def prepare(doc):
    """Pre-filter."""
    doc.tagline = False


def action(elem, doc):
    """Remove Vimwiki tag lines, e.g., :tag1:tag2:.

    Pandoc filter using panflute

    In-line tags in paragraphs and lists remain.
    """
    try:
        if (
            isinstance(elem, pf.Para)
            and isinstance(elem.content[0], pf.Span)
            and elem.content[-1].classes == ["tag"]
        ):
            return []
    except AttributeError:
        pf.debug(elem.content)
        raise AttributeError(
            "Vimwiki tagline should follow the item tagged. "
            "Try moving the tagline below the paragraph."
        )
    # return None -> element unchanged
    # return [] -> delete element
    return None


def finalize(doc):
    """Post-filter."""


def main(doc=None):
    """Remove taskwiki heading.

    Pandoc filter using panflute
    """
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
