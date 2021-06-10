"""Conftest.py for vimwiki_docx."""

import datetime
from pathlib import Path

import pytest

from vimwiki_docx.catvimwiki import catdiary, get_last_monday


@pytest.fixture(scope="module")
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
    wikidiary: Path = Path(__file__).parents[0] / "func/vimwiki/diary"
    enddate: datetime.date = datetime.date.fromisoformat(test_input)
    startdate: datetime.date = get_last_monday(enddate)
    return catdiary(startdate, enddate, wikidiary)
