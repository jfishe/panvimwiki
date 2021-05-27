"""Functional Tests pandoc filters Vimwiki files."""

import pytest

import pypandoc

from pathlib import Path

filter_input: Path = Path(__file__).parents[0] / "filters"
test_inputs = []
for test_input in filter_input.glob("*.wiki"):
    expected = test_input.with_suffix(".out.md")
    test_inputs.append((test_input, expected))


@pytest.mark.parametrize(
    "test_input, expected", test_inputs,
)
def test_pandoc_filter(test_input: Path, expected: Path):
    """Test pandoc python filters wiki to produce expected markdown.

    Assume filters/ contains filter_name.wiki and filter_name.out.md where
    filter_name.py is an installed console script.

    Parameters
    ----------
    test_input : Full path to filter_name.wiki

    expected : Full path to filter_name.out.md

    Returns
    -------
    None

    Raises
    ------
    TypeError : 'invalid api version', [1, 20]
                panflute requires pandoc-types >= 1.22
    """
    filters = [str(test_input.with_suffix(".py").name)]
    output = pypandoc.convert_file(
        str(test_input), to="markdown", format="vimwiki", filters=filters
    )
    with open(expected, mode="r") as fin:
        expected_output = fin.read()

    assert output == expected_output
