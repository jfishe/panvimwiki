"""Functional Tests concatenate Vimwiki diary files."""

import fileinput
import re
from pathlib import Path
from typing import List, Tuple


def search_not(diaryout: Path) -> Tuple[List[str], ...]:
    """Regex search for not & should appear, case-insensitive.

    Parameters
    ----------
    diaryout : Path to Vimwiki file

    Returns
    -------
    Lines containing not and lines containing 'should appear'. One result per
    line.

    """
    not_pattern = re.compile(r"not", re.IGNORECASE)
    should_pattern = re.compile(r"should appear|shouldappear", re.IGNORECASE)
    containsnot = []
    containsshould = []
    with fileinput.input(diaryout, openhook=fileinput.hook_encoded("utf-8")) as fin:
        for line in fin:
            research = re.search(not_pattern, line)
            if research is not None:
                containsnot.append(research.string)

            research = re.search(should_pattern, line)
            if research is not None:
                containsshould.append(research.string)

    return containsnot, containsshould


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
    containsnot, containsshould = search_not(catdiary_fixture)
    assert len(containsnot) == 21, containsnot
    assert len(containsshould) == 24, containsshould
