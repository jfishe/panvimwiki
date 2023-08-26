"""Conftest.py for panvimwiki."""

import datetime
from pathlib import Path
from typing import Generator

import pytest

from panvimwiki.catvimwiki import catdiary, get_last_monday


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
    # Setup
    test_input = "2017-04-27"
    wikidiary: Path = Path(__file__).parents[0] / "func/vimwiki/diary"
    enddate: datetime.date = datetime.date.fromisoformat(test_input)
    startdate: datetime.date = get_last_monday(enddate)
    wiki_output = catdiary(startdate, enddate, wikidiary)
    yield wiki_output

    # Teardown
    wiki_output.unlink()
