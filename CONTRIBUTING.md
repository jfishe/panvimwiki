# Contributing

Welcome to `panvimwiki` contributor's guide.

This document focuses on getting any potential contributor familiarized with
the development processes, but [other kinds of contributions] are also appreciated.

If you are new to using [git] or have never collaborated in a project
previously, please have a look at [contribution-guide.org]. Other resources are
also listed in the excellent [guide created by FreeCodeCamp] [^contrib1].

Please notice, all users and contributors are expected to be **open,
considerate, reasonable, and respectful**. When in doubt,
[Python Software Foundation's Code of Conduct] is a good reference in terms of
behavior guidelines.

## Issue Reports

If you experience bugs or general issues with `panvimwiki`, please have a look
on the [issue tracker]. If you don't see anything useful there, please feel
free to fire an issue report.

:::{tip}
Please don't forget to include the closed issues in your search.
Sometimes a solution was already reported, and the problem is considered
**solved**.
:::

New issue reports should include information about your programming environment
(e.g., operating system, Python version) and steps to reproduce the problem.
Please try also to simplify the reproduction steps to a very minimal example
that still illustrates the problem you are facing. By removing other factors,
you help us to identify the root cause of the issue.

## Documentation Improvements

You can help improve `panvimwiki` docs by making them more readable and
coherent, or by adding missing information and correcting mistakes.

`panvimwiki` documentation uses [Sphinx] as its main documentation compiler.
This means that the docs are kept in the same repository as the project code, and
that any documentation update is done in the same way was a code contribution,
e.g., [CommonMark] with [MyST] extensions.

[Panvimdoc] converts the README to Vim help format.

:::{tip}
Please notice that the [GitHub web interface] provides a quick way of
propose changes in `panvimwiki`'s files. While this mechanism can
be tricky for normal code contributions, it works perfectly fine for
contributing to the docs, and can be quite handy.

If you are interested in trying this method out, please navigate to
the `docs` folder in the source [repository], find which file you
would like to propose changes and click in the little pencil icon at the
top, to open [GitHub's code editor]. Once you finish editing the file,
please write a message in the form at the bottom of the page describing
which changes have you made and what are the motivations behind them and
submit your proposal.
:::

When working on documentation changes in your local machine, you can
compile them using [tox] :

```bash
tox -e docs
```

and use Python's built-in web server for a preview in your web browser
(`http://localhost:8000`):

```bash
python3 -m http.server --directory 'docs/_build/html' --bind localhost
```

Tox runs `make` and `pre-commit` to build Vim help documentation in
`doc/panvimwiki.txt`; you may need to run tox twice to resolve the following
`pre-commit` error message:

:::{error}
trim trailing whitespace.................................................Failed
:::

## Code Contributions

Pandoc filters rely on [Panflute](https://scorreia.com/software/panflute/) and
use the template
[located here](https://github.com/sergiocorreia/panflute/blob/master/docs/source/_static/template.py).

Plain text pre-filters follow a similar format but do not use `panflute`.

### Submit an issue

Before you work on any non-trivial code contribution it's best to first create
a report in the [issue tracker] to start a discussion on the subject.
This often provides additional considerations and avoids unnecessary work.

### Create an environment

Before you start coding, we recommend creating an isolated [virtual environment]
to avoid any problems with your installed Python packages.
This can easily be done via either [uv]:

```bash
uv venv [PATH TO VENV]
source [PATH TO VENV]/bin/activate
uv pip install --requirement requirements-dev.txt
```

or [Miniconda]:

```bash
conda env create --file=environment.yml
conda activate panvimwiki
```

### Clone the repository

1. Create an user account on GitHub if you do not already have one.

2. Fork the project [repository]: click on the *Fork* button near the top of the
   page. This creates a copy of the code under your account on GitHub.

3. Clone this copy to your local disk:

   ```bash
   git clone https://github.com/jfishe/panvimwiki.git
   cd panvimwiki
   ```

4. You should run:

   ```bash
   uv pip install --upgrade --editable .
   ```

   to be able to import the package under development in the Python REPL.

5. Install [pre-commit]:

   ```bash
   uv tool install pre-commit
   pre-commit autoupdate
   pre-commit install --install-hooks
   pre-commit install --hook-type commit-msg
   ```

   `panvimwiki` comes with a lot of hooks configured to automatically help the
   developer to check the code being written.

### Implement your changes

1. Create a branch to hold your changes:

   ```bash
   git checkout -b my-feature
   ```

   and start making changes. Never work on the main branch!

2. Start your work on this branch. Don't forget to add [docstrings] to new
   functions, modules and classes, especially if they are part of public APIs.

3. Add yourself to the list of contributors in `AUTHORS.md`.

4. When you’re done editing, do:

   ```bash
   git add [MODIFIED FILES]
   git commit
   ```

   to record your changes in [git].

   This project adheres to [Conventional Commits].
   The commit message should be structured as follows:

   ```text
   <type>[optional scope]: <description>

   [optional body]

   [optional footer(s)]
   ```

   Please make sure to see the validation messages from [pre-commit] and fix
   any eventual issues.
   This should automatically use [ruff] to check/fix the code style
   in a way that is compatible with the project.

   :::{important}
   Don't forget to add unit tests and documentation in case your
   contribution adds an additional feature and is not just a bugfix.

   Moreover, writing a [descriptive commit message] is highly recommended.
   In case of doubt, you can check the commit history with:

   ```bash
   git log --graph --decorate --pretty=oneline --abbrev-commit --all
   ```

   to look for recurring communication patterns.
   :::

5. Please check that your changes don't break any unit tests with:

   ```bash
   tox
   ```

   (after having installed [tox] with `uv tool install tox --with tox-uv`).

   You can also use [tox] to run several other pre-configured tasks in the
   repository. Try `tox -av` to see a list of the available checks.

### Submit your contribution

1. If everything works fine, push your local branch to the remote server with:

   ```bash
   git push -u origin my-feature
   ```

2. Go to the web page of your fork and click "Create pull request"
   to send your changes for review.

   Find more detailed information in [creating a PR]. You might also want to open
   the PR as a draft first and mark it as ready for review after the feedbacks
   from the continuous integration (CI) system or any required fixes.

### Troubleshooting

The following tips can be used when facing problems to build or test the
package:

1. Make sure to fetch all the tags from the upstream [repository].
   The command `git describe --abbrev=0 --tags` should return the version you
   are expecting. If you are trying to run CI scripts in a fork repository,
   make sure to push all the tags.
   You can also try to remove all the egg files or the complete egg folder, i.e.,
   `.eggs`, as well as the `*.egg-info` folders in the `src` folder or
   potentially in the root of your project.

2. Sometimes [tox] misses out when new dependencies are added, especially to
   `setup.cfg` and `docs/requirements.txt`. If you find any problems with
   missing dependencies when running a command with [tox], try to recreate the
   `tox` environment using the `-r` flag. For example, instead of:

   ```bash
   tox -e docs
   ```

   Try running:

   ```bash
   tox -r -e docs
   ```

3. Make sure to have a reliable [tox] installation that uses the correct
   Python version (e.g., 3.7+). When in doubt you can run:

   ```bash
   tox --version
   # OR
   which tox
   ```

   If you have trouble and are seeing weird errors upon running [tox], you can
   also try to create a dedicated [virtual environment] with a [tox] binary
   freshly installed. For example:

   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install tox tox-uv
   .venv/bin/tox -e all
   ```

4. [Pytest can drop you] in an interactive session in the case an error occurs.
   In order to do that you need to pass a `--pdb` option (for example by
   running `tox -- -k <NAME OF THE FALLING TEST> --pdb`).
   You can also setup breakpoints manually instead of using the `--pdb` option.

## Maintainer tasks

### Releases

If you are part of the group of maintainers and have correct user permissions
on [PyPI], the following steps can be used to release a new version for
`panvimwiki`:

1. Make sure all unit tests are successful.
2. Make sure Vim help is up to date, e.g., `tox -e docs`.
3. Update `RELEASE_HEAD.md`, [GitHub Actions] prepends to
   [releases].
4. Tag the current commit on the main branch with a release tag, e.g., `1.2.3`.
   NB: [GitHub Actions] release notes automation ignores `v1.2.3`,
   so drop the `v`.
5. Clean up the `dist` and `build` folders with `tox -e clean`
   (or `rm -rf dist build`)
   to avoid confusion with old builds and Sphinx docs.
6. Run `tox -e build` and check that the files in `dist` have
   the correct version (no `.dirty` or [git] hash) according to the [git] tag.
   Also check the sizes of the distributions, if they are too big (e.g., >
   500KB), unwanted clutter may have been accidentally included.
7. Push the new tag to the upstream [repository],
   e.g., `git push --tags`
8. [GitHub Actions] should run tests, upload to TestPyPI and [PyPI], and create
   a signed [release][releases].

[^contrib1]: Even though, these resources focus on open source projects and
    communities, the general ideas behind collaborating with other developers
    to collectively create software are general and can be applied to all sorts
    of environments, including private companies and proprietary code bases.

[commonmark]: https://commonmark.org/
[contribution-guide.org]: https://www.contribution-guide.org/
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/
[creating a pr]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
[descriptive commit message]: https://cbea.ms/git-commit/
[docstrings]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
[git]: https://git-scm.com
[github actions]: https://github.com/jfishe/panvimwiki/actions
[github web interface]: https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
[guide created by freecodecamp]: https://github.com/freecodecamp/how-to-contribute-to-open-source
[issue tracker]: https://github.com/jfishe/panvimwiki/issues
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
[myst]: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html
[other kinds of contributions]: https://opensource.guide/how-to-contribute
[panvimdoc]: https://github.com/kdheepak/panvimdoc
[pre-commit]: https://pre-commit.com/
[pypi]: https://pypi.org/
[pytest can drop you]: https://docs.pytest.org/en/stable/how-to/failures.html#dropping-to-pdb-on-failures
[python software foundation's code of conduct]: https://www.python.org/psf/conduct/
[releases]: https://github.com/jfishe/panvimwiki/releases
[repository]: https://github.com/jfishe/panvimwiki
[ruff]: https://github.com/astral-sh/ruff
[sphinx]: https://www.sphinx-doc.org/en/master/
[tox]: https://tox.wiki/
[uv]: https://github.com/astral-sh/uv
[virtual environment]: https://realpython.com/python-virtual-environments-a-primer/
