
## Description

Vimwiki_pandoc provides tools for conversion to Microsoft Word docx or other
output formats supported by
[Pandoc](https://pandoc.org/ "Pandoc a universal document converter").
Vimwiki_pandoc provides command line tools as well as Vim commands to
concatenate and convert Diary Notes or convert any Vimwiki note.

## Installation

``` bash
git clone https://github.com/jfishe/vimwiki_docx.git $HOME/.vim/pack/vimwiki/opt/vimwiki_pandoc
pushd $HOME/.vim/pack/vimwiki/start/vimwiki_pandoc
python -m pip install $HOME/.vim/pack/vimwiki/opt/vimwiki_pandoc
```

Vimwiki_pandoc requires Vim compiled with Python 3, so add the following to
'~/.vim/vimrc' prior to `filetype plugin indent on`. See |:packadd| for an
explanation.

``` vim
if has('python3')
  packadd! vimwiki_docx
endif
```

## Options

Optionally add the following to '~/.vim/vimrc' or, preferably,
'~/.vim/plugin/vimwiki.vim'. Vimwiki_pandoc defaults to docx format, without extra_args.
`g:wiki2pandoc_settings` 

``` vim
let g:wiki2pandoc_settings = {
      \ 'extra_args': [ '--shift-heading-level-by', '1',
      \ '--data-dir', '~/vimwiki_html/templates/'
      \ ],
      \ 'format': 'docx'
      \ }
```

## Development and Testing

Because pandoc is required a conda environment called `pyscaffold` is created.
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

## Commands

### Local Commands

These commands are only available (and meaningful) when you are currently in a
Vimwiki file.

`:VimwikiConvert[!]`
Convert the current DiaryNote (See |:VimwikiMakeDiaryNote|)
|buffer| to Microsoft Word docx format.Remove extraneous
info:

- Vimwiki tag lines, e.g., :tag1:tag2:
- Not started tasks, e.g., - [ ] Task1
- Non-task _ bullet lines, e.g., _ [[URI|Description]] or \*
  Text
- Remove empty parent/child headings.

Copy the path to the Word file to the clipboard register "+
|quoteplus|.

On Windows Subsystem for Linux (WSL), convert the path from
POSIX to Windows before copying to clipboard.

When the [!] is present, do not |:tabedit| the converted
DiaryNote and attempt to open the docx file with the default
program.

:VimwikiConvertWeek[!] _:VimwikiConvertWeek_
Concatentate the previous Monday through the current DiaryNote
(See |:VimwikiMakeDiaryNote|) |buffer| and convert to
Microsoft Word docx format.

    	Otherwise behave as `:VimwikiConvertToday`.

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.0.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
