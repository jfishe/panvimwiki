# wikilink_markdown

- [ ] task 1
      line 1.2
- [X] task 2
- [.] task 3
      line 3.2
  - [.] task 3.1
  - [.] task 3.2
- [[20231106-1619|Wiki Internal Link]]
- [[wn.home:index|Another's wiki cross-reference]]

```bash
cat wikilink_markdown.md |
pandoc \
  --from=commonmark_x+wikilinks_title_after_pipe \
  --standalone \
  --wrap=preserve \
  --to=commonmark_x |
mdformat --number \
  --extensions=wikilink \
  --extensions=myst \
  --extensions=simple_breaks - |
wikilink_markdown
```

@bloggs-jones discusses [@chomsky-73, p. 74].

Required `mdformat` extensions:

1. mdformat_wikilink: wikilink
2. mdformat_myst: myst installs,
   - mdformat_frontmatter: frontmatter
   - mdformat_footnote: footnote
   - mdformat_tables: tables
3. mdformat_simple_breaks: simple_breaks

---

::: {#refs .references .csl-bib-body .hanging-indent}
::: {#ref-bloggs-jones .csl-entry}
Bloggs, A. J., and X. Y. Jones. 1959. "Title Title Title Title Title Title Title Title Title Title." *Journal Journal Journal*.
:::

::: {#ref-chomsky-73 .csl-entry}
Chomsky, N. 1973. "Conditions on Transformations." In *A Festschrift for Morris Halle*, edited by S. R. Anderson and P. Kiparsky. New York: Holt, Rinehart & Winston.
:::
:::
