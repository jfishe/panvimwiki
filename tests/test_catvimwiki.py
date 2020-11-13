"""Test concatenate Vimwiki diary files."""

import datetime
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
        "2020-10-15", "2020-10-08", "2017-04-27",
    ],
)
def test_catdiary(test_input):
    """TODO: Docstring for test_catdiary.

    Parameters
    ----------
    function : TODO

    Returns
    -------
    TODO

    """
    enddate: datetime.date = datetime.date.fromisoformat(test_input)
    startdate: datetime.date = get_last_monday(enddate)
    diaryout: Path = catdiary(startdate, enddate)
    assert diaryout.exists
