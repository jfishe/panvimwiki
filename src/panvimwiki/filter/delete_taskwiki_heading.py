#!/usr/bin/env python3
"""Remove taskwiki heading.

Pandoc filter using panflute

Example
_______
bash> echo '== Taskwiki Viewports | should not appear | should not appear ==' |

bash> pandoc --from=vimwiki --to=markdown --filter=delete_taskwiki_heading

## Taskwiki Viewports {#Taskwiki Viewports }

"""

import re

import panflute as pf


def prepare(doc):
    """Pre-filter—do nothing."""


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
    """Post-filter—do nothing."""


def main(doc=None):
    """Remove taskwiki heading.

    Pandoc filter using panflute
    """
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
