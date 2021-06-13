"""Test stdio prefilters and pandoc filters for Markdown and Docx conversion."""

import filecmp
from pathlib import Path
import pypandoc

import pytest

from vimwiki_docx.convert import convert

PREFILTER = (
    "delete_bullet_star.py",
    "delete_task_pending.py",
)
FILTER = (
    "delete_empty_heading.py",
    "delete_tag_lines.py",
    "delete_taskwiki_heading.py",
)

RESULT_PATH: Path = Path(__file__).parents[0]


@pytest.mark.parametrize(
    "convert_expected, to",
    [
        pytest.param(RESULT_PATH / "convert.md", "markdown", id="markdown"),
        pytest.param(RESULT_PATH / "convert.docx", "docx", id="docx"),
    ],
)
def test_convert(
    catdiary_fixture: Path,
    convert_expected: Path,
    to: str,
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
