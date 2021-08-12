# Filter and convert Vimwiki notes using pandoc

## Introduction

Vimwiki_pandoc provides tools for conversion to Microsoft Word docx or other
output formats supported by
[Pandoc](https://pandoc.org/ "Pandoc a universal document converter").
Vimwiki_pandoc provides command line tools as well as Vim commands to
concatenate and convert Diary Notes or convert any Vimwiki note.

## Installation

Vimwiki_pandoc requires
[Pandoc](https://pandoc.org/ "Pandoc a universal document converter").
Installation with conda is recommended because the system version, e.g., with
Ubuntu, may be too old. Or download from the website.

Using the Vim 8 native packages, vimwiki_pandoc should install in
`pack/*/opt/vimwiki_pandoc` because it depends on `|python3|` and requires
installation of the python package vimwiki_pandoc.

From a bash shell, enter the following:

```bash
# Adjust dest to suit, e.g., $HOME/vimfiles/pack/vimwiki/opt/vimwiki_pandoc
dest="$HOME/.vim/pack/vimwiki/opt/vimwiki_pandoc"

git clone https://github.com/jfishe/vimwiki_docx.git "$dest"

# Activate the python environment used by Vim.
# Then install vimwiki_docx in that python environment.
python -m pip install "$dest"
```

Vimwiki_pandoc requires Vim compiled with Python 3, so add the following to
`|vimrc|` prior to `|:filetype-plugin-on|`. See `|:packadd|` for an
explanation. Otherwise, install vimwiki_pandoc in
`pack/*/start/vimwiki_pandoc`.

```vim
if has('python3')
  packadd! vimwiki_docx
endif
```

## Commands

### Command Line Shell

Vimwiki_pandoc provides plain text pre-filters and pandoc filters for use from
the command line.

#### Pre-filters

- `delete_bullet_star`: Remove unordered lists which use the star (asterisk)
  bullet marker. The pre-filter does not remove task list items (see
  `|delete_task_pending|`).

```bash
echo '- Bulleted list item 1 should appear\n' \
     '* Bulleted list item 6 should NOT appear' |
delete_bullet_star
```

```text
- Bulleted list item 6 should NOT appear
```

- `delete_task_pending`: Delete pending tasks.

```bash
echo '- [ ] Bulleted list done0 item 0 should NOT appear' \
     '- [.] Bulleted list done1 item 1 should appear' |
delete_task_pending
```

```text
- [.] Bulleted list done1 item 1 should appear
```

#### Pandoc Filters

- `delete_tag_lines`: Delete lines which only contain Vimwiki tags, e.g.,
  ':tag1:tag2:'

- `delete_empty_heading`: Remove headings that do not have any children or
  paragraphs. Remove tag lines first (`|delete_tag_lines|`) or the heading is
  not considered empty.

- `delete_taskwiki_heading`:

### Local Commands

These commands are only available (and meaningful) when you are currently in a
Vimwiki file.

#### VimwikiConvert

- `VimwikiConvert`: Convert the current Vimwiki buffer
- `VimwikiConvert!`: Convert and open with default viewer.

Convert the current Vimwiki `|buffer|` to the selected output format (default:
docx) specified in `|g:vimwiki_pandoc_settings|`.format.

Copy the path to the Word file to the clipboard register "+
`|quoteplus|`. On Windows Subsystem for Linux (WSL), convert the path from
POSIX to Windows before copying to clipboard.

Remove extraneous info:

- Vimwiki tag lines, e.g., :tag1:tag2:
- Not started tasks, e.g., - [ ] Task1
- Non-task _ bullet lines, e.g., _ [[URI|Description]] or \*
  Text
- Remove empty parent/child headings.

#### VimwikiConvertWeek

- `VimwikiConvertWeek`: Concatentate DiaryNotes for Monday through current
  buffer and convert.
- `VimwikiConvertWeek!`: Concatenate, convert and open in default viewer.

After concatenating DiaryNotes for the week, behave as `|VimwikiConvert|`.

## Options

### Settings

- `g:vimwiki_pandoc_settings`

  Optionally add the following to `|vimrc|` or, preferably,
  '~/.vim/plugin/vimwiki.vim'. Vimwiki_pandoc defaults to docx format, without extra_args.

```vim
let g:vimwiki_pandoc_settings = {
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
git clone https://github.com/jfishe/vimwiki_docx.git
cd vimwiki_docx
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

This project has been set up using PyScaffold 4.0.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
