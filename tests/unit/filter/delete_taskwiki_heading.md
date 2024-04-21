# Vimwiki with Taskwiki Content

* [[file:URI|Wikilinks URL should be converted]]
* [[d|Wikilinks URL should be converted]]

## Taskwiki Viewports | should not appear | should not appear

The heading should convert the Viewports should not.

### Taskwiki Preset Headers || should not appear || should not appear

The heading should convert the Preset should not.

``` bash
cat delete_taskwiki_heading.md |
  pandoc --from=markdown+wikilinks_title_after_pipe-task_lists-citations \
  --filter=delete_taskwiki_heading \
  --to=markdown > out/delete_taskwiki_heading.md.md
```
