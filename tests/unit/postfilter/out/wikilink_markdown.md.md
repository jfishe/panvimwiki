-   [ ] task 1
-   [X] task 2
-   [.] task 3
    -   [.] task 3.1
    -   [.] task 3.2
-   [Wiki Internal Link](20231106-1619)
-   [Another's wiki cross-reference](wn.home:index)

``` bash
pandoc --from=markdown+wikilinks_title_after_pipe-task_lists \
  --standalone \
  --wrap=none \
  --to=markdown
```
