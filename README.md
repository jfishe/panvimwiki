<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/panvimwiki.svg?branch=main)](https://cirrus-ci.com/github/<USER>/panvimwiki)
[![ReadTheDocs](https://readthedocs.org/projects/panvimwiki/badge/?version=latest)](https://panvimwiki.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/panvimwiki/main.svg)](https://coveralls.io/r/<USER>/panvimwiki)
[![PyPI-Server](https://img.shields.io/pypi/v/panvimwiki.svg)](https://pypi.org/project/panvimwiki/)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# Filter and convert Vimwiki notes using pandoc

## Introduction

Panvimwiki provides tools for conversion to Microsoft Word docx or other
output formats supported by
[Pandoc](https://pandoc.org/ "Pandoc a universal document converter").
Panvimwiki provides command line tools as well as Vim commands to
concatenate and convert Diary Notes or convert any Vimwiki note.

## Installation

Panvimwiki requires
[Pandoc](https://pandoc.org/ "Pandoc a universal document converter").
Installation with conda is recommended because the system version, e.g., with
Ubuntu, may be too old. Or download from the website.

Using the Vim 8 native packages, panvimwiki should install in
`pack/*/opt/panvimwiki` because it depends on [:python3](https://vimhelp.org/if_pyth.txt.html#python3)
and requires installation of the python package panvimwiki.

From a bash shell, enter the following:

```bash
# Adjust dest to suit, e.g., $HOME/vimfiles/pack/vimwiki/opt/panvimwiki
dest="$HOME/.vim/pack/vimwiki/opt/panvimwiki"

git clone https://github.com/jfishe/panvimwiki.git "$dest"

# Activate the python environment used by Vim.
# Then install panvimwiki in that python environment.
python -m pip install "$dest"
```

Panvimwiki requires Vim compiled with Python 3, so add the following to
[vimrc](https://vimhelp.org/starting.txt.html#vimrc)
prior to [:filetype-plugin-on](https://vimhelp.org/filetype.txt.html#%3Afiletype-plugin-on).
See [:packadd](https://vimhelp.org/repeat.txt.html#%3Apackadd)
for an explanation. Otherwise, install panvimwiki in `pack/*/start/panvimwiki`.

```vim
if has('python3')
  packadd! panvimwiki
endif
```

## Command Line Shell

Panvimwiki provides plain text pre-filters and pandoc filters for use from
the command line.

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
    "--shift-heading-level-by", "1",
    "--data-dir", str(Path.home() / "vimwiki_html/templates"),
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

### Pre-Filters

#### delete_bullet_star

Remove unordered lists which use the star (asterisk) bullet marker. The
pre-filter does not remove task list items (see [delete_task_pending](#delete_task_pending)).
The pre-filter does not handle wrapped bullets--i.e., it will delete the
bulleted-line and leave the wrapped lines. I haven't figured out a good regex
for wrapped lines.

```bash
echo '- Bulleted list item 1 should appear\n' \
     '* Bulleted list item 6 should NOT appear' |
delete_bullet_star
```

```text
- Bulleted list item 6 should NOT appear
```

#### delete_task_pending

Delete pending tasks.

```bash
echo '- [ ] Bulleted list done0 item 0 should NOT appear' \
     '- [.] Bulleted list done1 item 1 should appear' |
delete_task_pending
```

```text
- [.] Bulleted list done1 item 1 should appear
```

### Pandoc Filters

Panvimwiki provides plain text pre-filters and pandoc filters for use from
the command line.

#### delete_tag_lines

Delete lines which only contain Vimwiki tags, e.g., ':tag1:tag2:'

#### delete_empty_heading

Remove headings that do not have any children or paragraphs. Remove tag lines
first, [delete_tag_lines](#delete_tag_lines) or the heading is not considered empty.

#### delete_taskwiki_heading

## Commands

### Local Commands

These commands are only available (and meaningful) when you are currently in a
Vimwiki file.

#### VimwikiConvert[!]

Convert the current Vimwiki buffer. With !, open with default viewer.

Convert the current Vimwiki [:buffer](https://vimhelp.org/windows.txt.html#%3Abuffer)
to the selected output format (default: docx) specified in
[g:panvimwiki_settings](#gpanvimwiki_settings).format.

Copy the path to the Word file to the clipboard register "+
[quoteplus](https://vimhelp.org/gui_x11.txt.html#quoteplus).
On Windows Subsystem for Linux (WSL), convert the path from POSIX to Windows
before copying to clipboard.

Remove extraneous info:

- Vimwiki tag lines, e.g., :tag1:tag2:
- Not started tasks, e.g., - [ ] Task1
- Non-task bullet lines, e.g., `* [[URI|Description]]` or `* Text`
- Remove empty parent/child headings.

#### VimwikiConvertWeek[!]

Concatentate DiaryNotes for Monday through current buffer and convert.
With !, open in default viewer.

After concatenating DiaryNotes for the week, behave as [VimwikiConvert](#vimwikiconvert).

## Settings

### Global Settings

#### g:panvimwiki_settings

Optionally add the following to [vimrc](https://vimhelp.org/starting.txt.html#vimrc)
or, preferably, '~/.vim/plugin/vimwiki.vim'. Panvimwiki defaults to docx
format, without extra_args.

```vim
let g:panvimwiki_settings = {
      \ 'extra_args': [ '--shift-heading-level-by', '1',
      \ '--data-dir', '~/vimwiki_html/templates/'
      \ ],
      \ 'format': 'docx'
      \ }
```

## Development and Testing

Because pandoc is required, a conda environment called `pyscaffold` is created.
The default name may be overridden with the `--name <environment name>`
parameter.

```bash
git clone https://github.com/jfishe/panvimwiki.git
cd panvimwiki
conda env create --file environment.yml --name pyscaffold
conda activate pyscaffold
pipx install covimerage
```

Covimerage has conflicting dependencies, so pipx creates an isolated
executable in `~/.local/bin`. You may want to run `pipx uninstall covimerage`
to avoid cluttering `$PATH`.

```bash
tox -av # List tox commands and descriptions.
tox --recreate # Build the package and run tests with python and Vader.
tox -e vim # Run Vader tests and generate coverage report.
# Run Vader tests and view results with Vim.
vim -Nu tests/vim/vimrc -c 'Vader tests/vim/*.vader'
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
