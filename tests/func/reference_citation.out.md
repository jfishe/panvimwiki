---
date: "2023-09-16 07:36"
link-citations: true
references:
- author:
  - family: Bloggs
    given: A. J.
  - family: Jones
    given: X. Y.
  container-title: Journal journal journal
  id: bloggs-jones
  issued: 1959
  title: Title title title title title title title title title title
  type: article-journal
- author:
  - family: Chomsky
    given: N.
  container-title: A festschrift for Morris Halle
  editor:
  - family: Anderson
    given: S. R.
  - family: Kiparsky
    given: P.
  id: chomsky-73
  issued: 1973
  publisher: Holt, Rinehart & Winston
  publisher-place: New York
  title: Conditions on transformations
  type: paper-conference
tags: Zettelkasten
title: Try ZettelNew
type: note
---

```{=html}
<!-- pandoc --from=biblatex --to=markdown default.bib --standalone
pandoc --citeproc \
  --from=markdown+wikilinks_title_after_pipe \
  --standalone \
  --to=markdown-citations \
  --wrap=none -->
```
Hey [Adding to the House of Dude](230916-1043)

Bloggs and Jones ([1959](#ref-bloggs-jones))

([Chomsky 1973](#ref-chomsky-73))

------------------------------------------------------------------------

House of Dude


[#ref-bloggs-jones]: Bloggs, A. J., and X. Y. Jones. 1959. "Title Title Title Title Title Title Title Title Title Title." *Journal Journal Journal*.

[#ref-chomsky-73]: Chomsky, N. 1973. "Conditions on Transformations." In *A Festschrift for Morris Halle*, edited by S. R. Anderson and P. Kiparsky. New York: Holt, Rinehart & Winston.
