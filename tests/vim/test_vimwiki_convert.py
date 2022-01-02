"""Test Wiki2pandoc using Vader.vim."""

import subprocess
import shlex
from pathlib import Path


def test_vim_vader_all():
    """Run Vader.vim on *.vader.

    Pytest monitors python coverage and Vader runs Vim python modules--i.e., we
    don't have to mock `import vim`. `run.sh` runs without Pytest.
    """
    cwd: Path = Path(__file__).parents[0]
    vim_command = shlex.split(
        "vim -Nu tests/vim/vimrc -Es -c 'Vader! tests/vim/*.vader'"
    )
    test_input = subprocess.run(
        vim_command,
        capture_output=True,
        encoding="utf8",
        check=True,
    )
    print(test_input.stdout)
    print(test_input.stderr)
