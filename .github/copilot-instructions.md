# Copilot instructions for panvimwiki

Purpose
- Help Copilot sessions understand how to build, test, lint and navigate this repository.

Build / Test / Lint commands
- Setup (recommended): use uv (astral-sh/uv) or conda because pandoc is required by tests/docs:
  - uv venv --system-site-packages --python-preference=system
  - uv sync --all-extras --dev --group=testing
  - OR: conda env create --file environment.yml; conda activate panvimwiki
  - Install editable package for development: python -m pip install -e .

- Tox (primary task runner):
  - List tasks: tox -av
  - Recreate envs and run default tests: tox --recreate
  - Run specific python env (example): tox -e 3.14
  - Run a single tox env and forward pytest args: tox -e 3.14 -- tests/path/to/test_file.py::test_name

- Pytest (direct):
  - Run full test suite: pytest
  - Run a single test: pytest tests/test_module.py::test_function
  - Use -k <expr> to select tests by substring or marker: pytest -k name

- Make targets
  - make test  (runs Vader deps then pytest via Makefile)
  - make vimdoc (builds Vim help from README.md with pandoc)

- Vader (Vim) tests
  - Run Vader suite under tox with: tox -e vim
  - Or run from Vim: vim -Nu tests/vim/vimrc -c 'Vader tests/vim/*.vader'

- Linting / formatting
  - List linting tasks: tox -e lint  (uses prek/prek hooks in this repo)
  - ruff configuration is in pyproject.toml — ruff can be run directly (e.g., ruff src tests)
  - Markdown formatting and checks configured with mdformat and markdownlint in pyproject.toml

High-level architecture (big picture)
- Packaging: "src" layout; package name panvimwiki. Entry point scripts are defined in pyproject.toml under [project.scripts] (examples: delete_empty_heading, wikilink_markdown).
- Filters: panvimwiki.filter contains pandoc filters and plain-text pre-filters used by the CLI and Vim plugin.
- Vim integration: repo contains runtime Vim plugin pieces (after/, autoload/, plugin/, doc/) to be packaged/installed into Vim's runtimepath. Vim-specific tests use Vader under tests/vim.
- Docs: Sphinx-powered docs in docs/; README.md converts to Vim help using a pandoc-based toolchain (Makefile and build/panvimdoc). Docs and Vim help generation require pandoc and some lua filters.
- Test orchestration: tox creates isolated environments for multiple Python versions, runs pytest, and orchestrates Vader coverage steps. Makefile contains helper recipes to clone Vader and vimwiki into tests/vim/bundle and to symlink package pieces for Vader tests.

Key conventions and repository-specific patterns
- Use uv (astral-sh/uv) where README/Makefile refer to it for virtualenv and tool installs.
- Tests: pytest addopts (pyproject.toml) injects coverage options and verbose output; xfail_strict is enabled. Use pytest markers for selection (e.g., slow/system).
- Vim Vader tests must be run with Vim installed; the Makefile prepares a tests/vim/bundle with symlinks to the repo runtime files.
- Pre-commit and hooks: prek is used to manage hooks and checks (configured in tox -e lint). Ensure prek autoupdate / install hooks when setting up dev environment.
- Packaging: Project uses setuptools/pyproject.toml with setuptools_scm for versioning; keep source under src/.
- Conventional commits: repository expects Conventional Commits for PRs (see CONTRIBUTING.md).

Where to look first
- src/panvimwiki/filter.py (and submodules) for filter implementations
- tests/ and tests/vim/ for unit and Vader tests
- pyproject.toml, tox.ini and Makefile for CI, environment, test and doc build commands

CI notes
- Workflow files: check .github/workflows (notably .github/workflows/ci.yml) for exact CI steps.
- What CI runs: tests across multiple Python versions, documentation build, packaging (build) and publishing steps (TestPyPI/PyPI) on tagged releases per repo badges and CONTRIBUTING.md. Inspect the workflow file for details like which Python versions and which tox/test commands are executed.
- Reproducing CI locally: use tox to recreate the CI environment (tox --recreate or tox -e <env>) and ensure pandoc and vim are installed or available in PATH for docs/Vader steps. To reproduce a single CI job, run the tox env the workflow targets (e.g., tox -e 3.14) or run the exact pytest/tox command defined in the workflow.
- Secrets and releases: publishing steps require repository secrets (PyPI tokens); releases are created by tagging (follow CONTRIBUTING.md: tag without a leading 'v').
- Artifacts and reports: CI may upload coverage, build artifacts, or doc builds; check workflow for artifact names/paths.
- Fast checks for PRs: run tox -e lint and pytest -q locally before opening PR to match CI prechecks.

AI/assistant config files
- No other assistant config files (CLAUDE.md, AGENTS.md, .cursorrules, .windsurfrules, CONVENTIONS.md, AIDER_CONVENTIONS.md, .clinerules, .cline_rules) were detected in the repository root.

Notes for Copilot sessions
- When suggesting code changes that affect packaging/tests/docs, also update pyproject.toml, tox.ini or Makefile as needed and run tests locally (pytest/tox) because CI depends on them.
- For changes touching Vim integration, ensure Vader tests can run: Makefile's vader target creates required bundles and symlinks.
- When proposing changes that affect CI workflow files, include the minimal workflow diff and explain why environment versions, secrets, or artifact paths must change.

If you'd like this file adjusted (add examples, expand CI mapping to workflow jobs, or add MCP server configs), say which area to expand.
