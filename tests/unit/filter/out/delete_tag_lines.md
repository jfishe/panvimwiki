# Vimwiki Tag Lines and In-line Tags {#Vimwiki Tag Lines and In-line Tags}

In normal paragraphs
[]{#-InlineTagShouldAppear}[InlineTagShouldAppear]{#InlineTagShouldAppear
.tag}
[]{#-InlineTagShouldAppear}[InlineTagShouldAppear]{#InlineTagShouldAppear
.tag}

## Ordered List {#Ordered List}

1.  []{.done4}OrderedList done4 should appear with
    []{#-InlineTagShouldAppear}[InlineTagShouldAppear]{#InlineTagShouldAppear
    .tag}

### Unordered lists {#Unordered lists}

-   Bulleted list item 1 should appear
    []{#-InlineTagShouldAppear}[InlineTagShouldAppear]{#InlineTagShouldAppear
    .tag}
    []{#-InlineTagShouldAppear}[InlineTagShouldAppear]{#InlineTagShouldAppear
    .tag}

Multiple rows of tags should be deleted, when not part of a paragraph.

## Tag Lines and Definition lists {#Tag Lines and Definition lists}

[Hancock, John R.](mailto:Hancock, John R. <none@nowhere.org> "wikilink")
:   above the tagline. Pandoc pareses this as two paragraphs\--i.e.,
    taglines should always follow the tagged item.

## Tag Lines without hard breaks {#Tag Lines without hard breaks}

-   []{.done0}Taskwiki item
