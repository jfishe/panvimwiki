"""Unit Tests pandoc filters Vimwiki files."""

import pytest

import pypandoc

from pathlib import Path
from typing import List


def pandoc_filter_fixture():
    """Parameterize panflute filter script input and expected output.

    Assume filters/ contains filter_name.wiki and filter_name.out.md where
    filter_name.py is an installed console script that converts from the wiki
    to out.md.

    Returns
    -------
    List[pytest.param]

    """
    filter_input: Path = Path(__file__).parents[0] / "filters"
    test_inputs = []
    for test_input in filter_input.glob("*.wiki"):
        filters = str(test_input.with_suffix(".py").name)
        expected = test_input.with_suffix(".out.md")
        test_inputs.append(pytest.param(test_input, [filters], expected, id=filters))
    return test_inputs


@pytest.mark.parametrize(
    "test_input, filters, expected",
    pandoc_filter_fixture(),
)
def test_pandoc_filter(test_input: Path, filters: List[str], expected: Path):
    """Test pandoc python filters wiki to produce expected markdown.

    Parameters
    ----------
    test_input : Full path to filter_name.wiki

    filters : Panflute filter console_script(s)

    expected : Full path to filter_name.out.md

    Returns
    -------
    None

    Raises
    ------
    TypeError : 'invalid api version', [1, 20]
                panflute requires pandoc-types >= 1.22
    """
    output = pypandoc.convert_file(
        str(test_input), to="markdown", format="vimwiki", filters=filters
    )
    with open(expected, mode="r") as fin:
        expected_output = fin.read()

    assert output == expected_output
