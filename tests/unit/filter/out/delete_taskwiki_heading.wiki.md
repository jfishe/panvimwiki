# Vimwiki with Taskwiki Content

- [Wikilinks URL should be converted](file:URI)
- [Wikilinks URL should be converted](d){.wikilink}

## Taskwiki Viewports

The heading should convert the Viewports should not.

### Taskwiki Preset Headers

The heading should convert the Preset should not.

``` bash
cat tests/unit/filter/delete_taskwiki_heading.wiki |
  pandoc --from=vimwiki \
  --filter=delete_taskwiki_heading \
  --to=markdown > tests/unit/filter/out/delete_taskwiki_heading.wiki.md
```
