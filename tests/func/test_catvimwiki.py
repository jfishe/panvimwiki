"""Functional Tests concatenate Vimwiki diary files."""

import datetime
import fileinput
import re
from pathlib import Path
from typing import List

import pytest

from vimwiki_docx.catvimwiki import (
    catdiary,
    get_last_monday,
    del_empty_heading,
)


def search_not(diaryout: Path) -> List[str]:
    """Regex search for not, case-insensitive.

    Parameters
    ----------
    diaryout : Path to Vimwiki file

    Returns
    -------
    Lines containing not.

    """
    pattern = re.compile(r"not", re.IGNORECASE)
    containsnot = []
    with fileinput.input(diaryout, openhook=fileinput.hook_encoded("utf-8")) as fin:
        for line in fin:
            research = re.search(pattern, line)
            if research is not None:
                containsnot.append(research.string)

    return containsnot


@pytest.fixture
def catdiary_fixture() -> Path:
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
    wikidiary: Path = Path(__file__).parents[0] / "vimwiki/diary"
    enddate: datetime.date = datetime.date.fromisoformat(test_input)
    startdate: datetime.date = get_last_monday(enddate)
    return catdiary(startdate, enddate, wikidiary)


def test_catdiary(catdiary_fixture):
    """Test catdiary refilter removes all but 5 NOT lines.

    The test Vimwiki diary contains more than 5 NOT's, which refilter should
    remove. Leaving the rest for del_empty_heading to remove.

    Parameters
    ----------
    catdiary_fixture : Path
        Concatenated Vimwiki diary entries

    Returns
    -------
    None

    Raises
    ------
    AssertionError
        If concatenated diary does not contain 5x `not`.

    """
    containsnot = search_not(catdiary_fixture)
    assert len(containsnot) == 5, containsnot


def test_del_empty_heading(catdiary_fixture):
    """Test del_empty_heading removes all but 1 `not`.

    Remove `should NOT appear` empty headings.

    Parameters
    ----------
    catdiary_fixture : Path
        Concatenated Vimwiki diary entries

    Returns
    -------
    None

    """
    diaryout = del_empty_heading(catdiary_fixture)
    containsnot = search_not(diaryout)
    assert len(containsnot) == 1, containsnot


def test_no_del_empty_heading():
    """Test del_empty_heading does not modify Vimwiki file.

    Given the file does not contain empty headings, do not modify the file.

    Returns
    -------
    None

    """
    test_input = "2017-04-26"
    wikidiary: Path = Path(__file__).parents[0] / "vimwiki/diary"
    enddate: datetime.date = datetime.date.fromisoformat(test_input)
    startdate: datetime.date = enddate

    diaryout: Path = catdiary(startdate, enddate, wikidiary)
    modified = diaryout.stat().st_mtime

    diaryout = del_empty_heading(diaryout)

    assert modified == diaryout.stat().st_mtime
