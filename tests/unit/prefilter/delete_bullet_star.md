# Vimwiki Unordered Lists / Bulleted Lists Asterisk/Star

- Bulleted list item 1 should appear
- Bulleted list item 2 should appear :InlineTagShouldAppear:InlineTagShouldAppear:
- Bulleted list item 3 should appear
- [ ] Bulleted list done0 item 0 should appear
- [.] Bulleted list done1 item 1 should appear
- [o] Bulleted list done2 item 2 should appear
- [O] Bulleted list done3 item 3 should appear
- [X] Bulleted list done4 item 4 should appear
- [-] Bulleted list doneX item 5 should appear
* Bulleted list item 6 should NOT appear
* Bulleted list item 7 should NOT appear
* [ ] Bulleted list item 8 should NOT appear  #f2fbeb1b
* [.] Bulleted list item 9 should appear  #4a7369ae
* [S] Bulleted list item 10 should convert  #d6198091
* [W] Bulleted list item 11 should appear  #2da7eb9b
* [[file:URI|Bulleted list item 12 should NOT appear]]
* [[d|Bulleted list item 13 should NOT appear]]

``` bash
cat tests/unit/prefilter/delete_bullet_star.md | delete_bullet_star |
  pandoc --from=markdown+wikilinks_title_after_pipe-task_lists-citations \
  --to=markdown > tests/unit/prefilter/out/delete_bullet_star.md.md
```
