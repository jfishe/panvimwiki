# Vimwiki Tag Lines and In-line Tags

``` bash
cat delete_tag_lines.md |
  pandoc --from=markdown+wikilinks_title_after_pipe-task_lists-citations \
  --filter=delete_tag_lines \
  --to=markdown > out/delete_tag_lines.md.md
```

In normal paragraphs :InlineTagShouldAppear:InlineTagShouldAppear:

## Ordered List

:TagShouldNotAppear:TagShouldNotAppear2:

1. [X] OrderedList done4 should appear with
       :InlineTagShouldAppear:

### Unordered lists

- Bulleted list item 1 should appear :InlineTagShouldAppear:InlineTagShouldAppear:
  - Bulleted list item 2 should appear :InlineTagShouldAppear:InlineTagShouldAppear:

Multiple rows of tags should be deleted, when not part of a paragraph.

:TagShouldNotAppear:TagShouldNotAppear2:
:TagShouldNotAppear:TagShouldNotAppear2:

## Tag Lines and Definition lists

[[mailto:Hancock, John R. <none@nowhere.org>|Hancock, John R.]]
:   above the tagline. Pandoc pareses this as two paragraphs\--i.e.,
    taglines should always follow the tagged item.
:TagShouldNotAppear:TagShouldNotAppear2:

## Tag Lines without hard breaks

* [ ] Taskwiki item

:TagShouldNotAppear:TagShouldNotAppear2:
