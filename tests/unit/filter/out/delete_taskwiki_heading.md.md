# Vimwiki with Taskwiki Content

- [Wikilinks URL should be converted](file:URI){.wikilink}
- [Wikilinks URL should be converted](d){.wikilink}

## Taskwiki Viewports

The heading should convert the Viewports should not.

### Taskwiki Preset Headers

The heading should convert the Preset should not.

``` bash
cat tests/unit/filter/delete_taskwiki_heading.md |
  pandoc --from=markdown+wikilinks_title_after_pipe-task_lists-citations \
  --filter=delete_taskwiki_heading \
  --to=markdown > tests/unit/filter/out/delete_taskwiki_heading.md.md
```
