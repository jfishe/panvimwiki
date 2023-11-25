"""Test Wiki2pandoc using Vader.vim."""

import shlex
import subprocess


def test_vim_vader_all():
    """Run Vader.vim on *.vader.

    Pytest monitors python coverage and Vader runs Vim python modules--i.e., we
    don't have to mock `import vim`. `run.sh` runs without Pytest.
    Raise CalledProcessError if vim exits non-zero
    """
    vim_command = shlex.split(
        "vim -Nu tests/vim/vimrc -Es -c 'Vader! tests/vim/*.vader'"
    )
    test_input = subprocess.run(
        vim_command,
        capture_output=True,
        encoding="utf8",
        check=False,
    )
    print(test_input.stdout)
    print(test_input.stderr)

    test_input.check_returncode()
