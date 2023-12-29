---
title: Try ZettelNew
date: 2023-09-16 07:36
tags: Zettelkasten
type: note
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
---

Hey [Adding to the House of Dude](230916-1043)

```bash
# To convert BibLaTeX to Markdown Yaml Header above:
pandoc --from=biblatex --to=markdown default.bib --standalone

# To convert this file to expected output:
pandoc --citeproc \
  --from=markdown+wikilinks_title_after_pipe \
  --standalone \
  --to=markdown-citations+wikilinks_title_after_pipe  \
  --wrap=none \
  tests/func/reference_citation.md |
  reference_citation > tests/func/reference_citation.out.md
```

@bloggs-jones

[@chomsky-73]

[[vimwiki]]

----
House of Dude
