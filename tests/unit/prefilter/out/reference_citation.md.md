# Vimwiki convert pandoc references to reference links

``` bash
cat reference_citation.md | reference_citation |
  pandoc --from=markdown+wikilinks_title_after_pipe-task_lists-citations \
  --to=markdown > out/reference_citation.md.md
```

\[ref-bloggs-jones\]: Bloggs, A. J., and X. Y. Jones. 1959. "Title Title
Title Title Title Title Title Title Title Title." *Journal Journal
Journal*.

\[ref-chomsky-73\]: Chomsky, N. 1973. "Conditions on Transformations."
In *A Festschrift for Morris Halle*, edited by S. R. Anderson and P.
Kiparsky. New York: Holt, Rinehart & Winston.
