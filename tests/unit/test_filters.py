"""Unit Tests pandoc filters Vimwiki files."""

import pytest

import pypandoc

from pathlib import Path


def pandoc_filter_fixture():
    """Parameterize panflute filter script input and expected output.

    Assume filters/ contains filter_name.wiki and filter_name.out.md where
    filter_name.py is an installed console script that converts from .wiki to
    out.md.

    Raises
    ------
    TypeError : 'invalid api version', [1, 20]
                panflute requires pandoc-types >= 1.22

    """
    filter_input: Path = Path(__file__).parents[0] / "filters"

    for wiki_input in filter_input.glob("*.wiki"):
        filters = str(wiki_input.with_suffix(".py").name)

        test_input = pypandoc.convert_file(
            str(wiki_input), to="markdown", format="vimwiki", filters=[filters]
        )

        markdown_output = wiki_input.with_suffix(".out.md")
        with open(markdown_output, mode="r") as f:
            expected = f.read()

        yield pytest.param(test_input, expected, id=filters)


@pytest.mark.parametrize(
    "test_input, expected",
    pandoc_filter_fixture(),
)
def test_pandoc_filter(test_input: str, expected: str):
    """Test pandoc python filters wiki to produce expected markdown.

    Parameters
    ----------
    test_input : Converted Vimwiki to Markdown

    expected : Expected Markdown

    Returns
    -------
    None

    """
    assert test_input == expected
