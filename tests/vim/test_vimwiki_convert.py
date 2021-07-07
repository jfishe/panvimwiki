"""Test VimwikiConvert using Vader."""

import subprocess
import shlex
from pathlib import Path


def test_vimwiki_convert():
    """TODO: Docstring for test.

    Parameters
    ----------
    function : TODO

    Returns
    -------
    TODO

    """
    cwd: Path = Path(__file__).parents[0]
    vim_command = shlex.split("vim -Nu vimrc -Es -c 'Vader! VimwikiConvert.vader'")
    test_input = subprocess.run(
        vim_command, capture_output=True, encoding="utf8", check=True, cwd=cwd
    )
    print(test_input.stdout)
    print(test_input.stderr)
