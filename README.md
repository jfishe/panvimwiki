---
description: Filter and convert Vimwiki notes using pandoc.
project: panvimwiki
toc: true
vimversion: Vim v9.0
---

<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/panvimwiki.svg?branch=main)](https://cirrus-ci.com/github/<USER>/panvimwiki)
[![ReadTheDocs](https://readthedocs.org/projects/panvimwiki/badge/?version=latest)](https://panvimwiki.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/panvimwiki/main.svg)](https://coveralls.io/r/<USER>/panvimwiki)
[![PyPI-Server](https://img.shields.io/pypi/v/panvimwiki.svg)](https://pypi.org/project/panvimwiki/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/panvimwiki.svg)](https://anaconda.org/conda-forge/panvimwiki)
[![Monthly Downloads](https://pepy.tech/badge/panvimwiki/month)](https://pepy.tech/project/panvimwiki)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/panvimwiki)
-->

# Filter and convert Vimwiki notes using pandoc

[![Documentation Status][]][1] [![PyPI-Server][]][2] [![Test and Publish
Python 🐍 distribution 📦 to PyPI and TestPyPI][]][3] [![Project
generated with PyScaffold]][4]

## Introduction

Panvimwiki provides tools for conversion to Microsoft Word docx or other
output formats supported by [Pandoc] Panvimwiki provides command line
tools as well as Vim commands to concatenate and convert Diary Notes or
convert any Vimwiki note.

## Installation

Panvimwiki requires [Pandoc] Installation with `conda` is recommended
because the system version, e.g., with Ubuntu, may be too old. Or
download from the website. [Pypandoc] supports binary installation of
pandoc using `pip`.

Using the Vim 8 native packages, panvimwiki should install in
`pack/*/opt/panvimwiki` because it depends on [:python3] and requires
installation of the python package panvimwiki.

From a bash shell, enter the following:

```bash
# Adjust dest to suit, e.g., $HOME/vimfiles/pack/vimwiki/opt/panvimwiki
dest="$HOME/.vim/pack/vimwiki/opt/panvimwiki"

git clone https://github.com/jfishe/panvimwiki.git "$dest"

# Activate the python environment used by Vim.
# Then install panvimwiki in that python environment.
python -m pip install "$dest"
# Or to install from pypi:
python -m pip install panvimwiki
```

Panvimwiki requires Vim compiled with Python 3, so add the following to
[vimrc] prior to [:filetype-plugin-on]. See [:packadd] for an
explanation. Otherwise, install panvimwiki in `pack/*/start/panvimwiki`.

```vim
if has('python3')
  packadd! panvimwiki
endif
```

## Usage

### Command Line Shell

Panvimwiki provides plain text pre-filters and pandoc filters for use
from the command line.

For example from a bash prompt:

```bash
cat $HOME/vimwiki/diary/* |
    delete_bullet_star |
    delete_task_pending |
pandoc --from=vimwiki --to=markdown \
    --filter=delete_tag_lines \
    --filter=delete_taskwiki_heading \
    --filter=delete_empty_heading
```

From python:

```python
from pathlib import Path
from panvimwiki.convert import convert

PREFILTER = (
    "delete_bullet_star",
    "delete_task_pending",
)
FILTER = (
    "delete_tag_lines",
    "delete_empty_heading",
    "delete_taskwiki_heading",
)
EXTRA_ARGS = (
    "--shift-heading-level-by",
    "1",
    "--data-dir",
    str(Path.home() / "vimwiki_html/templates"),
)

convert(
    inputfile=str(Path.home() / "vimwiki/index.wiki"),
    outputfile=str(Path.home() / "vimwiki_html/markdown/index.md"),
    to="markdown",
    prefilters=PREFILTER,
    filters=FILTER,
    extra_args=EXTRA_ARGS,
)
```

#### Pre-Filters

##### delete_bullet_star

Remove unordered lists which use the star (asterisk) bullet marker.

The pre-filter does not remove task list items (see
[delete_task_pending]). The pre-filter does not handle wrapped
bullets--i.e., it will delete the bulleted-line and leave the wrapped
lines. I haven't figured out a good regex for wrapped lines.

```bash
echo '- Bulleted list item 1 should appear' \
     '* Bulleted list item 6 should NOT appear' |
delete_bullet_star
```

```text
- Bulleted list item 1 should appear
```

##### delete_task_pending

Delete pending tasks.

```bash
echo '- [ ] Bulleted list done0 item 0 should NOT appear' \
     '- [.] Bulleted list done1 item 1 should appear' |
delete_task_pending
```

```text
- [.] Bulleted list done1 item 1 should appear
```

#### Pandoc Filters

Panvimwiki provides plain text pre-filters, pandoc filters and
post-filters for use from the command line.

##### delete_tag_lines

Delete lines which only contain Vimwiki tags, e.g., ':tag1:tag2:'

##### delete_empty_heading

Remove headings that do not have any children or paragraphs. Remove tag
lines first, [delete_tag_lines] or the heading is not considered empty.

##### delete_taskwiki_heading

#### Post-Filters

##### reference_citation

Convert citations to a reference list.

`Example.md`:

```markdown
::: {#refs .references .csl-bib-body .hanging-indent}
::: {#ref-bloggs-jones .csl-entry}
Bloggs, A. J., and X. Y. Jones. 1959. "Title Title Title Title Title Title
Title Title Title Title." _Journal Journal Journal_.
:::

::: {#ref-chomsky-73 .csl-entry}
Chomsky, N. 1973. "Conditions on Transformations." In _A Festschrift for Morris
Halle_, edited by S. R. Anderson and P. Kiparsky. New York: Holt, Rinehart &
Winston.
:::
:::
```

`reference_citation < Example.md` produces:

```markdown
[#ref-bloggs-jones]: Bloggs, A. J., and X. Y. Jones. 1959. "Title Title Title Title
Title Title Title Title Title Title." _Journal Journal Journal_.

[#ref-chomsky-73]: Chomsky, N. 1973. "Conditions on Transformations." In _A
Festschrift for Morris Halle_, edited by S. R. Anderson and P. Kiparsky.
New York: Holt, Rinehart & Winston.
```

###### wikilink_markdown

Convert [Pandoc] markdown tasks and wikilinks to `:h vimwiki-todo-lists`
and markdown links compatible with `:h vimwiki-syntax-links`.

### Commands

#### Local Commands

These commands are only available (and meaningful) when you are
currently in a Vimwiki file.

##### VimwikiConvert\[!\]

Convert the current Vimwiki buffer. With !, open with default viewer.

Convert the current Vimwiki [:buffer] to the selected output format (default:
docx) specified in [g:panvimwiki_settings].

Copy the path to the Word file to the clipboard register "+ [quoteplus].
On Windows Subsystem for Linux (WSL), convert the path from POSIX to
Windows before copying to clipboard.

Remove extraneous info:

- Vimwiki tag lines, e.g., :tag1:tag2:
- Not started tasks, e.g., - \[ \] Task1
- Non-task bullet lines, e.g., `* [[URI|Description]]` or `* Text`
- Remove empty parent/child headings.

##### VimwikiConvertWeek\[!\]

Concatenate DiaryNotes for Monday through current buffer and convert.
With !, open in default viewer.

After concatenating DiaryNotes for the week, behave as [VimwikiConvert].

##### VimwikiReference

If in markdown format, expand [Pandoc Citations] in the current file and
append to the end of the file. The Yaml metadata should [specify the
bibliographic data] and the [Citation Style Language (CSL)].

Add the following to `.markdownlint.yml` to suppress `MD033`:

```yaml
# MD033/no-inline-html : Inline HTML :
# https://github.com/DavidAnson/markdownlint/blob/main/doc/md033.md
MD033:
  # MD033/no-inline-html Inline HTML [Element: div]
  # Allowed elements
  allowed_elements:
    - 'div'
```

`VimwikiReference` overwrites the file, so Vim may prompt to reload the
buffer (cf. Warning `:h W12`). If you choose not to reload the buffer,
`:h :DiffOrig` facilitate review of the changes.

##### VimwikiMarkdownFormat

If in markdown format, convert `:h vimwiki-syntax-links`
[wikilinks_title_after_pipe](https://pandoc.org/MANUAL.html#extension-wikilinks_title_after_pipe)
to [Inline links](https://pandoc.org/MANUAL.html#inline-links), without the
"wikilink" title that pandoc adds by default. Preserve `:h vimwiki-todo-lists`,
using [task_lists](https://pandoc.org/MANUAL.html#inline-linksInline).

`VimwikiMarkdownFormat` overwrites the file, so Vim may prompt to reload the
buffer (cf. Warning `:h W12`). If you choose not to reload the buffer,
`:h :DiffOrig` facilitate review of the changes.

### Settings

#### Global Settings

##### g:panvimwiki_settings

Optionally add the following to or, preferably,
'\~/.vim/plugin/vimwiki.vim'. Panvimwiki defaults to docx format,
without extra_args.

```vim
let g:panvimwiki_settings = {
      \ 'extra_args': [ '--shift-heading-level-by', '1',
      \ '--data-dir', '~/vimwiki_html/templates/'
      \ ],
      \ 'format': 'docx'
      \ }
```

## Development and Testing

Because pandoc is required, a conda environment called `panvimwiki` is
created. The default name may be overridden with the
`--name <environment name>` parameter.

```bash
git clone https://github.com/jfishe/panvimwiki.git
cd panvimwiki
conda env create --file environment.yml
conda activate panvimwiki
```

```bash
tox -av # List tox commands and descriptions.
tox --recreate # Build the package and run tests with python and Vader.
tox -e vim # Run Vader tests and generate coverage report.
# Run Vader tests and view results with Vim.
vim -Nu tests/vim/vimrc -c 'Vader tests/vim/*.vader'
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see <https://pyscaffold.org/>.

<!-- References -->

[Documentation Status]: https://readthedocs.org/projects/panvimwiki/badge/?version=latest
[1]: https://panvimwiki.readthedocs.io/en/latest/?badge=latest
[PyPI-Server]: https://img.shields.io/pypi/v/panvimwiki.svg
[2]: https://pypi.org/project/panvimwiki/
[Test and Publish Python 🐍 distribution 📦 to PyPI and TestPyPI]: https://github.com/jfishe/panvimwiki/actions/workflows/ci.yml/badge.svg
[3]: https://github.com/jfishe/panvimwiki/actions/workflows/ci.yml
[Project generated with PyScaffold]: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
[4]: https://pyscaffold.org/
[Pandoc]: https://pandoc.org/
[Pypandoc]: https://github.com/JessicaTegner/pypandoc?tab=readme-ov-file#installing-via-pip
[:python3]: https://neovim.io/doc/user/if_pyth.html#python3
[vimrc]: https://neovim.io/doc/user/starting.html
[:filetype-plugin-on]: https://neovim.io/doc/user/filetype.html#filetype
[:packadd]: https://neovim.io/doc/user/repeat.html#%3Apackadd
[delete_task_pending]: #delete_task_pending
[delete_tag_lines]: #delete_tag_lines
[:buffer]: https://neovim.io/doc/user/windows.html#%3Abuffer
[quoteplus]: https://neovim.io/doc/user/provider.html#quoteplus
[VimwikiConvert]: #vimwikiconvert
[Pandoc Citations]: https://pandoc.org/MANUAL.html#citation-syntax
[specify the bibliographic data]: https://pandoc.org/MANUAL.html#specifying-bibliographic-data
[Citation Style Language (CSL)]: https://pandoc.org/MANUAL.html#specifying-a-citation-style
<!-- markdownlint-disable MD051 -->
[g:panvimwiki_settings]: #g-panvimwiki-settings
