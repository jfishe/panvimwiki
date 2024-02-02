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
    postfilter_input: Path = Path(__file__).parents[0] / "postfilter"

    for wiki_input in chain(
        prefilter_input.glob("*.wiki"),
        filter_input.glob("*.wiki"),
        postfilter_input.glob("*.inmd"),
    ):
        filter = str(wiki_input.stem)

        if prefilter_input == wiki_input.parent:
            with open(wiki_input) as fin:
                filter_out = subprocess.run(
                    filter, capture_output=True, encoding="utf8", stdin=fin, check=True
                )

            test_input = pypandoc.convert_text(
                str(filter_out.stdout), to="markdown", format="vimwiki"
            )
            filter = "plain_text_pre_filter/" + filter
        elif filter_input == wiki_input.parent:
            test_input = pypandoc.convert_file(
                str(wiki_input), to="markdown", format="vimwiki", filters=[filter]
            )
            filter = "pandoc_filter/" + filter
        elif postfilter_input == wiki_input.parent:
            stdin = pypandoc.convert_file(
                source_file=wiki_input,
                format="markdown+wikilinks_title_after_pipe-task_lists",
                to="markdown",
                extra_args=("--standalone", "--wrap", "none"),
            )
            filter_out = subprocess.run(
                filter, capture_output=True, encoding="utf8", input=stdin, check=True
            )

            test_input = filter_out.stdout
            filter = "plain_text_post_filter/" + filter
            __import__("pprint").pprint(test_input)
        else:
            continue

        markdown_output = wiki_input.with_suffix(".out.md")
        with open(markdown_output) as f:
            expected = f.read()

        __import__("pprint").pprint(expected)
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


def test_delete_tag_lines_disorder():
    """test_delete_tag_lines_disorder.

    Given tagline above tagged paragraph, raise AttributeError with helpful
    error message.
    """
    tagline = (
        r":TagShouldNotAppear:TagShouldNotAppear2:"
        "\n"
        r"[[mailto:Hancock, John R. <none@nowhere.org>|Hancock, John R.]]:: "
        r"below the tagline. "
        r"Pandoc Vimwiki reader parses this as one paragraph, "
        r"with a Softbreak between."
        "\n"
    )
    match = (
        "Vimwiki tagline should follow the item tagged. "
        "Try moving the tagline below the paragraph."
    )
    with pytest.raises(RuntimeError, match=match) as excinfo:
        pypandoc.convert_text(
            tagline,
            to="markdown",
            format="vimwiki",
            filters=["delete_tag_lines"],
            encoding="utf8",
        )
    assert "AttributeError" in str(excinfo.value)
