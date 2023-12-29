"""Test stdio prefilters and pandoc filters for Markdown and Docx conversion."""

from __future__ import annotations

import filecmp
from pathlib import Path

import pypandoc
import pytest

from panvimwiki.convert import convert

RESULT_PATH: Path = Path(__file__).parents[0]
DATA_DIR: Path = RESULT_PATH / "vimwiki_html/templates"

PREFILTER = (
    "delete_bullet_star",
    "delete_task_pending",
)
FILTER = (
    "delete_tag_lines",
    "delete_empty_heading",
    "delete_taskwiki_heading",
)
EXTRA_ARGS = (
    "--shift-heading-level-by",
    "1",
    "--data-dir",
    str(DATA_DIR),
    "--verbose",
)

FILTER_WITH_WRONG_ORDER = (
    "delete_empty_heading",
    "delete_tag_lines",
    "delete_taskwiki_heading",
)


@pytest.mark.parametrize(
    "convert_expected, to, extra_args, filters, postfilters",
    [
        pytest.param(
            RESULT_PATH / "convert.md",
            "markdown",
            None,
            FILTER,
            None,
            id="markdown",
        ),
        pytest.param(
            RESULT_PATH / "convert.md",
            "markdown",
            None,
            FILTER_WITH_WRONG_ORDER,
            None,
            id="filter_disorder",
            marks=pytest.mark.xfail(
                reason="delete_empty_heading before delete_tag_lines",
            ),
        ),
        pytest.param(
            RESULT_PATH / "convert.docx",
            "docx",
            None,
            FILTER,
            None,
            id="docx",
        ),
        pytest.param(
            RESULT_PATH / "convert_shift.md",
            "markdown",
            EXTRA_ARGS,
            FILTER,
            None,
            id="markdown_extra_args",
        ),
        pytest.param(
            RESULT_PATH / "convert_shift.docx",
            "docx",
            EXTRA_ARGS,
            FILTER,
            None,
            id="docx_extra_args",
        ),
        pytest.param(
            RESULT_PATH / "convert_shift.md",
            "markdown",
            EXTRA_ARGS,
            FILTER,
            ("reference_citation",),
            id="markdown_extra_args_no_citeproc",
        ),
    ],
)
def test_convert(
    catdiary_fixture: Path,
    convert_expected: Path,
    to: str,
    extra_args: tuple,
    filters: tuple,
    postfilters: tuple | None,
):
    """Test prefilters and filters in series against expected output."""
    # Setup
    suffix: str = convert_expected.suffix
    outputfile: Path = catdiary_fixture.with_suffix(suffix)

    convert(
        inputfile=str(catdiary_fixture),
        outputfile=str(outputfile),
        to=to,
        prefilters=PREFILTER,
        filters=filters,
        postfilters=postfilters,
        extra_args=extra_args,
    )

    if to == "docx":
        test_input = pypandoc.convert_file(
            str(outputfile), to="markdown", format="docx"
        )
        expected = pypandoc.convert_file(
            str(convert_expected), to="markdown", format="docx"
        )
        assert test_input == expected
    else:
        assert filecmp.cmp(outputfile, convert_expected, shallow=False)

    # Teardown
    outputfile.unlink()


def test_convert_postfilter(tmp_path):
    r"""Given Markdown with pandoc citeproc references,

    When pypandoc.convert_text and postfilter reference_citation applied,
    Then return expected references as reference links.

    pandoc --from=biblatex --to=markdown default.bib --standalone
    pandoc --citeproc \
      --from=markdown+wikilinks_title_after_pipe \
      --standalone \
      --to=markdown-citations \
      --wrap=none
    """
    convert_expected = RESULT_PATH / "reference_citation.out.md"
    inputfile = RESULT_PATH / "reference_citation.md"
    with convert_expected.open() as f:
        expected = f.read()
    test_input = convert(
        inputfile=str(inputfile),
        outputfile=None,
        format="markdown+wikilinks_title_after_pipe",
        to="markdown-citations+wikilinks_title_after_pipe",
        prefilters=None,
        filters=None,
        extra_args=(
            "--citeproc",
            "--standalone",
            "--wrap",
            "none",
        ),
        postfilters=("reference_citation",),
    )
    print(test_input)
    assert test_input == expected
