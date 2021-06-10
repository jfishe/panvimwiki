"""Test stdio prefilters and pandoc filters for Markdown and Docx conversion."""

import subprocess
from pathlib import Path
import pypandoc
import pytest

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
    "prefilters, prefilter_expected, filters, filter_expected",
    [
        pytest.param(
            PREFILTER,
            RESULT_PATH / "convert.wiki",
            FILTER,
            RESULT_PATH / "convert.md",
            id="pandoc filters markdown",
        ),
    ],
)
def test_convert_markdown(
    prefilters, prefilter_expected, filters, filter_expected, catdiary_fixture
):
    """TODO: Docstring for test.

    Parameters
    ----------
    function : TODO

    Returns
    -------
    TODO

    """
    with open(catdiary_fixture, mode="r", encoding="utf8") as fin:
        test_input = fin.read()

    for cmd in prefilters:
        filter_out = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            input=test_input,
            check=True,
        )
        test_input = filter_out.stdout

    with open(prefilter_expected) as fin:
        expected: str = fin.read()

    assert test_input == expected

    test_input = pypandoc.convert_text(
        test_input, to="markdown", format="vimwiki", filters=filters
    )

    with open(filter_expected) as fin:
        expected: str = fin.read()

    assert test_input == expected
