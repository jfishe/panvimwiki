# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Removed

## [0.8.0] - 2024-02-24

### Added

- `Markdowlint` `YAML` configuration.
- `pre-commit` `markdownlint-cli`

### Changed

- `VimwikiReference` and `expand_citeproc()` reference anchors use GitHub
  Flavored Markdown (gfm) to minimize `markdownlint` errors:
  - Fix `MD051/link-fragments`
  - Accept `MD033/no-inline-html`.
- `wikilink_markdown` filter converts pandoc tasks to `taskwiki` format.
- Preserve citations when converting `:h vimwiki-syntax-links`.
- Copyright date
- Adopt [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.7.1] - 2024-01-28

- Add `:VimwikiMarkdownFormat` to convert `:h vimwiki-syntax-links` to markdown
  and preserve any `:h vimwiki-todo-lists`.
- Add post-filter `wikilink_markdown` to convert pandoc markdown tasks to
  Vimwiki Todo lists and markdown "wikilinks" to Vimwiki compatible links.
- Remove intermediary autoload functions. Call Python 3 functions directly from
  `:VimwikiReference` and `:VimwikiTaskLink`.

## [0.7] - 2024-01-13

- `:VimwikiReference` no longer converts to reference-links, preferring
  compatibility with pandoc conversion to `HTML`.
- DOCS: Update `:help panvimwiki`.
- DOCS: Host at <http://panvimwiki.readthedocs.io/>

## [0.6] - 2024-01-01

- Vim command `:VimwikiReference` converts
  [Pandoc Citations](https://pandoc.org/MANUAL.html#citation-syntax)
  to [reference links](https://pandoc.org/MANUAL.html#reference-links),
  e.g.,`[anchor:]`, replacing the current file.
- DOCS: Update `:help`.
- BUILD: Use pre-commit to remove trailing spaces from Vim help.

## [0.5] - 2023-12-04

- Vim command `:VimwikiReference` converts `citeproc` entries and appends to
  current buffer.
- Add `reference_citation` to expand `citeproc` entries in markdown with
  [vim-zettel](https://github.com/michal-h21/vim-zettel)
- DOCS: add contributing guide.
- BUILD: Update `panvimdoc` and build Vim help file with tox.
- BUILD: Upgrade to `pyscaffold` v4.5.
- BUILD: Add `pre-commit`.

## [0.4.0] - 2022-10-30

- Rename project and package: panvimwiki
- Add Makefile to build Vim help from Markdown using `panvimdoc`.
- Pass `$TMP` in tox.ini, so concatenated diary files do not clutter project
  tree, because when `$TMP` does not exist, use the current working directory.
- Wiki2pandoc replicates relative path in out—i.e.,
  `~/vimwiki/diary/2017-04-04.wiki` becomes
  `~/vimwiki_html/docx/diary/2017-04-04.docx`.
- Use covimerage to provide coverage for vader tests.

## [0.3.0] - 2021-07-07

- Switch documentation to Markdown.
- Add panflute and regex filters. Processing can happen solely from the command
  line.
- Add Vader.vim tests to bring coverage to 100%.
- Vim commands `VimwikiConvert` and `VimwikiConvertWeek` default to
  `~/vimwiki_html/docx/prepm.docx`, rather than `$TMP/prepm.docx`.

## [0.2.0] - 2021-05-11

- Switch build to pyscaffold.
- Vim :help vimwiki_pandoc
- Pydoc to view python module help.
- FIX: prevent taskwiki changes to diary during conversion to docx.

## [0.1.0] - 2021-05-01

- Switch build to flit.

[unreleased]: https://github.com/jfishe/panvimwiki/compare/0.8.0...HEAD
[0.8.0]: https://github.com/jfishe/panvimwiki/compare/0.7.1...0.8.0
[0.7.1]: https://github.com/jfishe/panvimwiki/compare/0.7...0.7.1
[0.7]: https://github.com/jfishe/panvimwiki/compare/0.6...0.7
[0.6]: https://github.com/jfishe/panvimwiki/compare/0.5...0.6
[0.5]: https://github.com/jfishe/panvimwiki/compare/0.4.0...0.5
[0.4.0]: https://github.com/jfishe/panvimwiki/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/jfishe/panvimwiki/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/jfishe/panvimwiki/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/jfishe/panvimwiki/releases/tag/0.1.0
