"""Unit Tests pandoc filters Vimwiki files."""

import subprocess
from itertools import chain
from pathlib import Path

import pypandoc
import pytest


def pandoc_filter_fixture():
    """Parameterize panflute filter script input and expected output.

    Assume filter/ contains filter_name.wiki and filter_name.out.md where
    filter_name.py is an installed console script that converts from .wiki to
    out.md.

    Raises
    ------
    TypeError : 'invalid api version', [1, 20]
                panflute requires pandoc-types >= 1.22

    """
    prefilter_input: Path = Path(__file__).parents[0] / "prefilter"
    filter_input: Path = Path(__file__).parents[0] / "filter"

    for wiki_input in chain(
        prefilter_input.glob("*.wiki"), filter_input.glob("*.wiki")
    ):
        filter = str(wiki_input.with_suffix(".py").name)

        if prefilter_input == wiki_input.parent:
            with open(wiki_input, mode="r") as fin:
                filter_out = subprocess.run(
                    filter, capture_output=True, encoding="utf8", stdin=fin, check=True
                )

            test_input = pypandoc.convert_text(
                str(filter_out.stdout), to="markdown", format="vimwiki"
            )
        else:
            test_input = pypandoc.convert_file(
                str(wiki_input), to="markdown", format="vimwiki", filters=[filter]
            )

        markdown_output = wiki_input.with_suffix(".out.md")
        with open(markdown_output, mode="r") as f:
            expected = f.read()

        yield pytest.param(test_input, expected, id=filter)


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
