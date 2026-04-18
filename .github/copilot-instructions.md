# Copilot instructions for panvimwiki

Purpose

- Help Copilot sessions understand how to build,
  test, lint and navigate this repository.

Build / Test / Lint commands

- Setup (recommended): use uv (astral-sh/uv) or
  conda because pandoc is required by tests/docs.

  Example with uv:

  ```bash
  uv venv --system-site-packages \
    --python-preference=system
  uv sync --all-extras \
    --dev --group=dev --group=testing
  uv pip install --upgrade --editable .
  ```

  Example with conda:

  ```bash
  conda env create --file environment.yml
  conda activate panvimwiki
  uv pip install --group=dev \
    --group=testing -e .
  ```

- Tox (primary task runner):

  - List tasks: `tox -av`
  - Recreate envs and run default tests:
    `tox --recreate`
  - Run specific python env (example): `tox -e 3.14`
  - Run a single tox env and forward pytest args:

  ```bash
  tox -e 3.14 -- \
    tests/path/to/test_file.py::test_name
  ```

- Pytest (direct):

  - Run full test suite: `pytest`
  - Run a single test:
    `pytest tests/test_module.py::test_function`
  - Use `-k <expr>` to select tests by substring
    or marker: `pytest -k name`

- Make targets

  ```bash
  make test    # runs Vader deps then pytest via Makefile
  make vimdoc  # builds Vim help from README.md with pandoc
  ```

- Vader (Vim) tests

  - Run Vader suite under tox: `tox -e vim`

  Or run the Vader tests from Vim:

  ```vim
  vim -Nu tests/vim/vimrc \
    -c 'Vader tests/vim/*.vader'
  ```

- Linting / formatting

  - List linting tasks: `tox -e lint` (uses `prek` hooks)
  - Ruff can be run directly, e.g.: `ruff src tests`
  - Markdown formatting and checks are configured
    with mdformat and markdownlint (see `pyproject.toml`)

High-level architecture (big picture)

- Packaging: "src" layout; package name panvimwiki.
  Entry point scripts live in pyproject.toml under
  [project.scripts] (examples: delete_empty_heading,
  wikilink_markdown).

- Filters: panvimwiki.filter contains pandoc filters
  and plain-text pre-filters used by the CLI and the
  Vim plugin.

- Vim integration: runtime pieces are in after/,
  autoload/, plugin/, doc/. Those are packaged and
  installed into Vim's runtimepath. Vader tests live
  under tests/vim.

- Docs: Sphinx-powered docs in docs/. README.md is
  converted to Vim help via a pandoc-based toolchain
  (Makefile and build/panvimdoc). Pandoc and Lua
  filters are required.

- Test orchestration: tox creates isolated envs for
  multiple Python versions, runs pytest, and
  orchestrates Vader coverage steps. The Makefile
  provides helpers to prepare Vader and vimwiki
  bundles for tests.

Key conventions and repository-specific patterns

- Use uv (astral-sh/uv) for environment and tool
  management as referenced in README and Makefile.

- Tests: pytest addopts (pyproject.toml) enables
  coverage flags and verbose output. xfail_strict is
  enabled. Use pytest markers (e.g., slow, system)
  when needed.

- Vim/Vader: Vader tests require a system Vim. The
  Makefile prepares tests/vim/bundle and symlinks
  package runtime files during testing.

- Pre-commit and hooks: prek manages hooks and checks.
  Run `prek autoupdate` and install hooks during setup.

- Packaging: setuptools_scm is used for versioning.
  Keep sources under src/.

- Conventional commits: project follows Conventional
  Commits for PR messages (see CONTRIBUTING.md).

Where to look first

- src/panvimwiki/filter.py (and submodules)
- tests/ and tests/vim/ for unit and Vader tests
- pyproject.toml, tox.ini, Makefile for CI and docs

CI notes

- Workflow files live under .github/workflows.
  Inspect ci.yml for exact job steps.

- CI runs tests across Python versions, builds docs,
  builds package artifacts and (on tags) publishes
  to TestPyPI/PyPI. Check the workflow for details.

- Reproduce CI locally with tox (`tox --recreate`) and
  ensure pandoc and vim are available for docs/Vader.

- Secrets: publishing steps require PyPI tokens (GH
  secrets). Releases are created by tagging without
  a leading `v`.

- Artifacts/reports: CI uploads coverage, build
  artifacts and docs. Check artifact names/paths in
  the workflow.

AI/assistant config files

- No other assistant config files were detected in
  the repository root (CLAUDE.md, AGENTS.md, etc.).

Notes for Copilot sessions

- When suggesting changes that affect packaging,
  tests, or docs, update pyproject.toml, tox.ini, or
  Makefile accordingly and run tests locally.

- For changes touching Vim integration, ensure Vader
  tests are runnable; use Makefile's vader target to
  prepare bundles and symlinks.

- When proposing changes to CI workflows, include a
  minimal workflow diff and document required changes
  to environments, secrets, or artifact paths.

If you'd like this file adjusted
(add examples, expand CI mapping to workflow jobs, or add MCP server configs),
say which area to expand.
