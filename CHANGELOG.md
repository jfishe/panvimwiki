# Changelog

## Version 0.4 (development)

- Rename project and package: panvimwiki
- Add Makefile to build Vim help from Markdown using `panvimdoc`.
- Pass `$TMP` in tox.ini, so concatenated diary files do not clutter project
  tree, because when `$TMP` does not exist, use the current working directory.
- Wiki2pandoc replicates relative path in out—i.e.,
  `~/vimwiki/diary/2017-04-04.wiki` becomes
  `~/vimwiki_html/docx/diary/2017-04-04.docx`.
- Use covimerage to provide coverage for vader tests.

## Version 0.3 (2021-07-07)

- Switch documentation to Markdown.
- Add panflute and regex filters. Processing can happen solely from the command
  line.
- Add Vader.vim tests to bring coverage to 100%.
- Vim commands `VimwikiConvert` and `VimwikiConvertWeek` default to
  `~/vimwiki_html/docx/prepm.docx`, rather than `$TMP/prepm.docx`.

## Version 0.2 (2021-05-11)

- Switch build to pyscaffold.
- Vim :help vimwiki_pandoc
- Pydoc to view python module help.
- FIX: prevent taskwiki changes to diary during conversion to docx.

## Version 0.1 (2021-05-01)

- Switch build to flit.
