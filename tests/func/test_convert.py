"""Test stdio prefilters and pandoc filters for Markdown and Docx conversion."""

import filecmp
from pathlib import Path
from typing import Tuple

import pypandoc
import pytest

from vimwiki_docx.convert import convert

RESULT_PATH: Path = Path(__file__).parents[0]
DATA_DIR: Path = RESULT_PATH / "vimwiki_html/templates"

PREFILTER = (
    "delete_bullet_star.py",
    "delete_task_pending.py",
)
FILTER = (
    "delete_empty_heading.py",
    "delete_tag_lines.py",
    "delete_taskwiki_heading.py",
)
EXTRA_ARGS = (
    "--shift-heading-level-by",
    "1",
    "--data-dir",
    str(DATA_DIR),
    "--verbose",
)


@pytest.mark.parametrize(
    "convert_expected, to, extra_args",
    [
        pytest.param(RESULT_PATH / "convert.md", "markdown", None, id="markdown"),
        pytest.param(RESULT_PATH / "convert.docx", "docx", None, id="docx"),
        pytest.param(
            RESULT_PATH / "convert_shift.md",
            "markdown",
            EXTRA_ARGS,
            id="markdown_extra_args",
        ),
        pytest.param(
            RESULT_PATH / "convert_shift.docx", "docx", EXTRA_ARGS, id="docx_extra_args"
        ),
    ],
)
def test_convert(
    catdiary_fixture: Path,
    convert_expected: Path,
    to: str,
    extra_args: Tuple,
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
        filters=FILTER,
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
