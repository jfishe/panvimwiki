- [ ] task 1
- [X] task 2
- [.] task 3
  - [.] task 3.1
  - [.] task 3.2
- [[20231106-1619|Wiki Internal Link]]
- [[wn.home:index|Another's wiki cross-reference]]

```bash
pandoc --from=markdown+wikilinks_title_after_pipe-task_lists \
  --standalone \
  --wrap=none \
  --to=markdown-citations | wikilink_markdown
```

---

::: {#refs .references .csl-bib-body .hanging-indent}
::: {#ref-bloggs-jones .csl-entry}
Bloggs, A. J., and X. Y. Jones. 1959. "Title Title Title Title Title Title Title Title Title Title." *Journal Journal Journal*.
:::

::: {#ref-chomsky-73 .csl-entry}
Chomsky, N. 1973. "Conditions on Transformations." In *A Festschrift for Morris Halle*, edited by S. R. Anderson and P. Kiparsky. New York: Holt, Rinehart & Winston.
:::
:::
