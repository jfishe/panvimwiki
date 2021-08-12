"""Unit Tests concatenate Vimwiki diary files."""

import datetime
from typing import Tuple

import pytest

from panvimwiki.catvimwiki import catdiary, get_last_monday, get_last_thursday


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (get_last_monday(), datetime.date),
        (get_last_thursday(), datetime.date),
    ],
)
def test_get_last_default(test_input: str, expected: str):
    """Test get_last_monday or thursday default parameters."""
    assert type(test_input) is expected


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
        ("2017-04-27", "2017-04-26"),
    ],
)
def test_catdiary_start_gt_end(test_input: Tuple[str, str]):
    """Given startdate after enddate, catdiary should raise ValueError.

    Parameters
    ----------
    test_input : ISO format date (startdate, enddate)

    Returns
    -------
    None

    """
    startdate = datetime.date.fromisoformat(test_input[0])
    enddate = datetime.date.fromisoformat(test_input[1])

    with pytest.raises(ValueError):
        catdiary(startdate, enddate)
