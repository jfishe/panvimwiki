"""Test stdio prefilters and pandoc filters for Markdown and Docx conversion."""

import filecmp
from pathlib import Path
from typing import Tuple

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
    "convert_expected, to, extra_args, filters",
    [
        pytest.param(
            RESULT_PATH / "convert.md", "markdown", None, FILTER, id="markdown"
        ),
        pytest.param(
            RESULT_PATH / "convert.md",
            "markdown",
            None,
            FILTER_WITH_WRONG_ORDER,
            id="filter_disorder",
            marks=pytest.mark.xfail(
                reason="delete_empty_heading before delete_tag_lines",
            ),
        ),
        pytest.param(RESULT_PATH / "convert.docx", "docx", None, FILTER, id="docx"),
        pytest.param(
            RESULT_PATH / "convert_shift.md",
            "markdown",
            EXTRA_ARGS,
            FILTER,
            id="markdown_extra_args",
        ),
        pytest.param(
            RESULT_PATH / "convert_shift.docx",
            "docx",
            EXTRA_ARGS,
            FILTER,
            id="docx_extra_args",
        ),
    ],
)
def test_convert(
    catdiary_fixture: Path,
    convert_expected: Path,
    to: str,
    extra_args: Tuple,
    filters: Tuple,
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
