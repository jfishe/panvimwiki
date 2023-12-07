#!/usr/bin/env python3
r"""
Convert citations to a reference list.

Plain text filter

Pandoc reads a markdown file with citeproc references to a BibLaTeX or other
supported database. The markdown output conflicts with Markdownlint.
`reference_citation` converts the reference list to
`Reference links <https://pandoc.org/MANUAL.html#reference-links>`_.

.. code-block:: bash

  pandoc --citeproc \
    --bibliography=default.bib \
    --metadata='link-citations:true' \
    --from=markdown+wikilinks_title_after_pipe \
    --standalone \
    --to=markdown-citations \
    --wrap=none \
    example.md |
  reference_citation

Example
-------
Create a Pandoc markdown file, e.g., `example.md`, with citeproc references.

.. code-block:: markdown

  @bloggs-jones

  [@chomsky-73]

  [[Chomsky 1973|@chomsky-73]]

A citeproc compatible database, e.g., BibLaTeX `default.bib`.

.. code-block:: bibtex

  @Article{bloggs-jones,
    author =       "A. J. Bloggs and X. Y. Jones",
    title =        "Title title title title title title title title title title",
    journal =      "Journal journal journal",
    year =         "1959",
  }

  @Inproceedings{chomsky-73,
    author =       "N. Chomsky",
    year =         "1973",
    title =        "Conditions on Transformations",
    booktitle =    "A festschrift for {Morris Halle}",
    editor =       "S. R. Anderson and P. Kiparsky",
    publisher =    "Holt, Rinehart \& Winston",
    address =      "New York",
  }

Pandoc outputs markdown citation format.

.. code-block:: markdown

  ::: {#refs .references .csl-bib-body .hanging-indent}
  ::: {#ref-bloggs-jones .csl-entry}
  Bloggs, A. J., and X. Y. Jones. 1959. "Title Title Title Title Title Title Title Title Title Title." *Journal Journal Journal*.
  :::

  ::: {#ref-chomsky-73 .csl-entry}
  Chomsky, N. 1973. "Conditions on Transformations." In *A Festschrift for Morris Halle*, edited by S. R. Anderson and P. Kiparsky. New York: Holt, Rinehart & Winston.
  :::
  :::

`reference_citation` converts to reference link format. The anchor uses #tag
format.

.. code-block:: markdown

  [#bloggs-jones]: Bloggs, A. J., and X. Y. Jones. 1959. "Title Title Title Title Title Title Title Title Title Title." *Journal Journal Journal*.

  [#chomsky-73]: Chomsky, N. 1973. "Conditions on Transformations." In *A Festschrift for Morris Halle*, edited by S. R. Anderson and P. Kiparsky. New York: Holt, Rinehart & Winston.

"""  # noqa: E501

from __future__ import annotations

import re
import sys


def filter_reference(source: str | None = None) -> str | None:
    """Convert pandoc citeproc CSL references to explicit reference links.

    `Reference links <https://pandoc.org/MANUAL.html#reference-links>`_.
    """
    if source is None:
        source = sys.stdin.read()
        isstdio = True
    else:
        isstdio = False

    lines = []
    for result in re.findall("::: {#ref-(.*?):::", source, re.S):
        entry = result.split("\n")
        reference = f"[#{entry[0].split()[0]}]:"
        citation = "\n".join(entry[1:])
        lines.append(f"{reference} {citation}")
    lines = "\n".join(lines)

    if isstdio:
        print(lines)
        return None
    return lines


if __name__ == "__main__":
    filter_reference()
