"""Convert str dates to datetime and Path. Set default days for missing dates."""

from __future__ import annotations

import datetime
from pathlib import Path

from panvimwiki.catvimwiki import catdiary, get_last_monday, get_last_thursday


def concatenate_diary(
    diary_path: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> Path:
    """Concatenate Vimwiki diary from start_date through end_date.

    If the start and end dates are None, concatenate Vimwiki Diary from
    Monday - Thursday. E.g., Thursday through Sunday returns this week.
    Monday - Wednesday returns last week.

    Parameters
    ----------
    diary_path
        Vimwiki Diary absolute path

    start_date
        ISO date, e.g., '2017-10-10', the same or earlier than `end_date`.
        Defaults to the previous Monday before `end_date`, unless `end_date` is
        Monday.

    end_date
        ISO date, e.g., '2017-10-10', defaults to the previous Thursday before
        today, unless today is Thursday.

    Returns
    -------
    pathlib.Path
        Path to concatenated Vimwiki diary file

    Raises
    ______
    ValueError
        `catdiary()` raises ValueError if `start_date` is after `end_date`

    """
    if end_date is None:
        enddate: datetime.date = get_last_thursday()
    else:
        enddate = datetime.date.fromisoformat(end_date)

    if start_date is None:
        startdate: datetime.date = get_last_monday(enddate)
    else:
        startdate = datetime.date.fromisoformat(start_date)

    if diary_path:
        wikidiary: Path = Path(diary_path)
    else:
        raise ValueError(f"{diary_path=}. A valid diary path is required.")

    return catdiary(startdate=startdate, enddate=enddate, wikidiary=wikidiary)
