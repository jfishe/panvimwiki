"""Conftest.py for vimwiki_docx."""

import datetime
import pypandoc
import subprocess
from pathlib import Path
import pytest
from typing import Generator

from vimwiki_docx.catvimwiki import catdiary, get_last_monday


@pytest.fixture(scope="function")
def catdiary_fixture() -> Generator[Path, None, None]:
    """Concatenate Vimwiki diary entries two non-contiguous days.

    Concatenate `vimwiki/diary/2017-04-24.wiki` and
    `vimwiki/diary/2017-04-26.wiki`. When provided enddate 2017-04-27
    Use get_last_monday(test_input) for startdate. Should not fail when other
    days between Monday and Thursday are missing.

    Returns
    -------
    Path to concatenated Vimwiki diary

    """
    test_input = "2017-04-27"
    wikidiary: Path = Path(__file__).parents[0] / "func/vimwiki/diary"
    enddate: datetime.date = datetime.date.fromisoformat(test_input)
    startdate: datetime.date = get_last_monday(enddate)
    wiki_output = catdiary(startdate, enddate, wikidiary)
    yield wiki_output
    wiki_output.unlink()


PREFILTER = (
    "delete_bullet_star.py",
    "delete_task_pending.py",
)
FILTER = (
    "delete_empty_heading.py",
    "delete_tag_lines.py",
    "delete_taskwiki_heading.py",
)

RESULT_PATH: Path = Path(__file__).parents[0] / "func"


@pytest.fixture()
def convert_fixture(
    catdiary_fixture,
    prefilters=PREFILTER,
    prefilter_expected=RESULT_PATH / "convert.wiki",
    filters=FILTER,
    filter_expected=RESULT_PATH / "convert.md",
):
    """Pytest Fixture apply prefilters and pandoc filters."""
    with open(catdiary_fixture, mode="r", encoding="utf8") as fin:
        test_input = fin.read()

    # Prefilter
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

    pytest_param = [pytest.param(test_input, expected, id="prefilter")]

    # Pandoc Filter
    test_input = pypandoc.convert_text(
        test_input, to="markdown", format="vimwiki", filters=filters
    )

    with open(filter_expected) as fin:
        expected = fin.read()

    pytest_param.append(pytest.param(test_input, expected, id="filter markdown"))

    return pytest_param
