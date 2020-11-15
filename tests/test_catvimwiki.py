"""Test concatenate Vimwiki diary files."""

import datetime
import fileinput
import re
from pathlib import Path

import pytest

from vimwiki_docx.catvimwiki import catdiary, get_last_monday, get_last_thursday


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2020-10-31", "2020-10-29"),
        ("2020-11-01", "2020-10-29"),
        ("2020-10-29", "2020-10-29"),
        ("2020-10-28", "2020-10-22"),
    ],
)
def test_get_last_thursday(test_input: str, expected: str):
    """Test get_last_thursday."""
    today: datetime.date = datetime.date.fromisoformat(test_input)
    thursday: datetime.date = datetime.date.fromisoformat(expected)
    assert thursday == get_last_thursday(today=today)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2020-10-31", "2020-10-26"),
        ("2020-10-26", "2020-10-26"),
    ],
)
def test_get_last_monday(test_input: str, expected: str):
    """Test get_last_monday."""
    today: datetime.date = datetime.date.fromisoformat(test_input)
    monday: datetime.date = datetime.date.fromisoformat(expected)
    assert monday == get_last_monday(today=today)


@pytest.mark.parametrize(
    "test_input",
    [
        "2017-04-27",
    ],
)
def test_catdiary_20170427(test_input):
    """Concatenate Vimwiki diary entries two non-contiguous days.

    Concatenate `vimwiki/diary/2017-04-24.wiki` and
    `vimwiki/diary/2017-04-26.wiki`. When provided enddate 2017-04-27
    Use get_last_monday(test_input) for startdate. Should not error when other
    days between Monday and Thursday are missing.

    Parameters
    ----------
    test_input : ISO format date 2017-04-27.

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If concatenated diary contains `not`, more than once.

    """
    wikidiary: Path = Path(__file__).parents[0] / "vimwiki/diary"
    enddate: datetime.date = datetime.date.fromisoformat(test_input)
    startdate: datetime.date = get_last_monday(enddate)
    diaryout: Path = catdiary(startdate, enddate, wikidiary)

    pattern = re.compile(r"not", re.IGNORECASE)
    containsnot = []
    with fileinput.input(diaryout, openhook=fileinput.hook_encoded("utf-8")) as fin:
        for line in fin:
            research = re.search(pattern, line)
            if research is not None:
                containsnot.append(research.string)
    assert len(containsnot) == 1, containsnot
