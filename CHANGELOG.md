---
reference-links: true
---

# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to
[Semantic Versioning].

## [Unreleased]

### Added

### Fixed

### Changed

### Removed

## [0.11.0] - 2025-07-06

### Added

- GitHub Action `CSchoel/release-notes-from-changelog`
- Adopt [Conventional Commits]
  via `pre-commit` with `gitlint`.

### Fixed

- `after/ftplugin/vimwiki.vim` clobbers `b:undo_ftplugin`.
- `reference_citation` output should not include leading `#`.
- Neovim does not load plugin: Remove check for 'patch-8.2.0578h'.

### Changed

- For compatibility with [MyST], replace `gfm` with `commonmark_x` for
  Markdown output, when:
  - Converting vimwiki-syntax-links and
  - Expanding citations.
- For [MyST] compatibility, `wikilink_markdown` formats pandoc Markdown
  output with [mdformat] including:
  - [mdformat_myst],
  - [mdformat_simple_breaks], and
  - [mdformat-wikilink].
- Support [Semantic Line Breaks] by changing default [pandoc]
  default from `--wrap=none` to `--wrap=preserve` in
  `:he VimwikiMarkdownFormat` and `:he VimwikiReference`.
- Constrain conda `environment.yml`, pandoc versions and vim to match Github
  Actions default Ubuntu.
- Github Actions and expected tests to match pandoc 3.7 output.

## [0.10.1] - 2024-11-06

### Added

- Conquer of Completion (CoC) can complete
  [Vim-Zettel] YAML front_matter
  fields:
  - `type:` note, literature, reference, or index.
  - `status:` Create, Process, or Reviewed.
- Pre-commit with [Vimjas/vint].

### Fixed

- Issue #2. Change `delete_taskwiki_heading` to remove anchors and work for
  markdown and vimwiki syntax.
- `tox -e linkcheck` errors.
- v0.10.0, fix incorrect version of `pypa/gh-action-pypi-publish`.

### Changed

- `VimwikiConvert` supports Vimwiki Markdown syntax (Issue #2).
- Duplicate unit tests for Vimwiki default and markdown syntax. Include in the
  input file a command line invocation to produce expected output.
- `wiki2pandoc` (`:VimwikiReference` and `:VimwikiMarkdownFormat`) from
  `--wrap=auto` to None because Vimwiki syntax does not allow wrapping in
  links, unlike pandoc.
- Pre-commit replace python pyupgrade, flake8, isort, black, and
  blacken-docs with `ruff` and fix `ruff` and `PyRight` errors.
- Move `ruff` and `markdownlint-cli` configuration to `pyproject.toml`.
- GitHub Actions update versions.
- Pandoc update to v3.5.
- Conda remove tox-conda and unused packages.
- Tox update to v4.23.2.

### Removed

- Replace UltiSnips Snippets for Zettelkasten YAML with Conquer of Completion
  (CoC).

## [0.9.0] - 2024-03-24

### Added

- UltiSnips Snippets for Zettelkasten YAML:
  - `type:` Type first letter to pick: note, literature, reference, or index.
  - `status:` Type first letter to pick: Create, Process, or Reviewed.

### Changed

- `:VimwikiMarkdownFormat` converts to GitHub Flavored Markdown (gfm) preferred
  by Vimwiki.
- `:VimwikiMarkdownFormat` preserves citations and does not process through
  citeproc to separate concerns from `:VimwikiReference`.
- Post-filter `reference_citation` supports pandoc v3.1.3 and v3.1.12.3
  `markdown-citations`. `pandoc --citeproc` default markdown-citations format
  changed from `:::` to `:::::` before and after citations. However, tests only
  support v3.1.12.3.
- `:VimwikiReference` defaults to link-citations=true and autowrap=auto.
- GitHub Actions updated to pandoc-version 3.1.12.3.

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
- Adopt [Keep a Changelog].

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
- DOCS: Host at <https://panvimwiki.readthedocs.io/>

## [0.6] - 2024-01-01

- Vim command `:VimwikiReference` converts
  [Pandoc Citations]
  to [reference links],
  e.g.,`[anchor:]`, replacing the current file.
- DOCS: Update `:help`.
- BUILD: Use pre-commit to remove trailing spaces from Vim help.

## [0.5] - 2023-12-04

- Vim command `:VimwikiReference` converts `citeproc` entries and appends to
  current buffer.
- Add `reference_citation` to expand `citeproc` entries in markdown with
  [vim-zettel]
- DOCS: add contributing guide.
- BUILD: Update `panvimdoc` and build Vim help file with tox.
- BUILD: Upgrade to `pyscaffold` v4.5.
- BUILD: Add `pre-commit`.

## [0.4.0] - 2022-10-30

- Rename project and package: panvimwiki
- Add Makefile to build Vim help from Markdown using `panvimdoc`.
- Pass `$TMP` in tox.ini, so concatenated diary files do not clutter project
  tree, because when `$TMP` does not exist, use the current working directory.
- Wiki2pandoc replicates relative path in out---i.e.,
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

[0.1.0]: https://github.com/jfishe/panvimwiki/releases/tag/0.1.0
[0.10.1]: https://github.com/jfishe/panvimwiki/compare/0.9.0...0.10.1
[0.11.0]: https://github.com/jfishe/panvimwiki/compare/0.10.1...0.11.0
[0.2.0]: https://github.com/jfishe/panvimwiki/compare/0.1.0...0.2.0
[0.3.0]: https://github.com/jfishe/panvimwiki/compare/0.2.0...0.3.0
[0.4.0]: https://github.com/jfishe/panvimwiki/compare/0.3.0...0.4.0
[0.5]: https://github.com/jfishe/panvimwiki/compare/0.4.0...0.5
[0.6]: https://github.com/jfishe/panvimwiki/compare/0.5...0.6
[0.7]: https://github.com/jfishe/panvimwiki/compare/0.6...0.7
[0.7.1]: https://github.com/jfishe/panvimwiki/compare/0.7...0.7.1
[0.8.0]: https://github.com/jfishe/panvimwiki/compare/0.7.1...0.8.0
[0.9.0]: https://github.com/jfishe/panvimwiki/compare/0.8.0...0.9.0
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/
[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[mdformat]: https://pypi.org/project/mdformat/
[mdformat-wikilink]: https://pypi.org/project/mdformat-wikilink/
[mdformat_myst]: https://pypi.org/project/mdformat_myst/
[mdformat_simple_breaks]: https://pypi.org/project/mdformat_simple_breaks/
[myst]: https://mystmd.org/
[pandoc]: https://pandoc.org/
[pandoc citations]: https://pandoc.org/MANUAL.html#citation-syntax
[reference links]: https://pandoc.org/MANUAL.html#reference-links
[semantic line breaks]: https://sembr.org/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
[unreleased]: https://github.com/jfishe/panvimwiki/compare/0.11.0...HEAD
[vim-zettel]: https://github.com/michal-h21/vim-zettel
[vimjas/vint]: https://github.com/Vimjas/vint
