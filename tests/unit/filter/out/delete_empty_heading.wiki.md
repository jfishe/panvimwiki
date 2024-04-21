# Vimwiki with and without Empty Headings {#Vimwiki with and without Empty Headings}

## Text {#Text}

``` bash
cat delete_empty_heading.wiki |
  pandoc --from=vimwiki \
  --filter=delete_empty_heading \
  --to=markdown > out/delete_empty_heading.wiki.md
```

Normal text should appear with only one blank line preceding next
heading.

## Empty Parent Heading with Non-Empty Child should appear {#Empty Parent Heading with Non-Empty Child should appear}

### Non-Empty Child Heading should appear {#Non-Empty Child Heading should appear}

Non-Empty Child text should appear.
