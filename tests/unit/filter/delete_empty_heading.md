# Vimwiki with and without Empty Headings

## Text


```bash
cat delete_empty_heading.md |
  pandoc --from=markdown+wikilinks_title_after_pipe-task_lists-citations \
  --filter=delete_empty_heading \
  --to=markdown > out/delete_empty_heading.md.md
```

Normal text should appear with only one blank line preceding next heading.


## Empty Heading with multiple blank lines should NOT appear


## Empty Parent Heading with empty child heading should NOT appear 2

### Empty Child Heading should NOT appear 3

#### Empty Child Heading should NOT appear 4

##### Empty Child Heading should NOT appear 5

###### Empty Child Heading should NOT appear 6

## Empty Parent Heading with Non-Empty Child should appear

### Non-Empty Child Heading should appear

Non-Empty Child text should appear.

### Empty heading at EOF should NOT appear
