"""Concatenate Vimwiki diary files."""

import datetime
import fileinput
import os
from pathlib import Path

from dateutil.relativedelta import MO, TH, relativedelta


def get_last_thursday(today: datetime.date = None) -> datetime.date:
    """Return datetime for closest Thursday before today.

    Parameters
    ----------
    today
        Any date object

    Returns
    -------
    datetime.date
        Previous Thursday before today, unless today is Thursday.

    """
    if today is None:
        today = datetime.date.today()
    return today + relativedelta(weekday=TH(-1))


def get_last_monday(today: datetime.date = None) -> datetime.date:
    """Return datetime for closest Monday before today.

    Parameters
    ----------
    today
        Any date object

    Returns
    -------
    datetime.date
        Previous Monday before today, unless today is Monday.

    """
    if today is None:
        today = datetime.date.today()
    return today + relativedelta(weekday=MO(-1))


def catdiary(
    startdate: datetime.date,
    enddate: datetime.date,
    wikidiary: Path = None,
) -> Path:
    """Concatenate Vimwiki diary files.

    Assume diary wiki files are named using ISO date, e.g., `2021-06-09.wiki`.

    Parameters
    ----------
    startdate
        Starting date for Vimwiki diary entry.

    enddate
        End date date for Vimwiki diary entry.

    wikidiary
        Path to Vimwiki diary directory. Defaults to `$HOME/vimwiki/diary`.

    Returns
    -------
    pathlib.Path
        Path to concatenated Vimwiki diary entries from startdate to enddate,
        inclusive of both.

    Raises
    ______
    ValueError
        If `startdate` is after `enddate`

    """
    if wikidiary is None:
        wikidiary = Path.home() / "vimwiki/diary"

    if startdate > enddate:
        errmsg = f"enddate {enddate} should not precede startdate {startdate}."
        raise ValueError(errmsg)

    diaryin = sorted(
        day
        for day in wikidiary.glob("[0-9]*.wiki")
        if startdate <= datetime.date.fromisoformat(day.stem) <= enddate
    )
    if not diaryin:
        raise OSError(f"Diary not found at {wikidiary=}")

    tmppath: str = os.getenv("TMP", os.getcwd())
    diaryout: Path = Path(tmppath) / "prepm.wiki"

    with open(diaryout, "w", encoding="utf8") as fout, fileinput.input(
        files=diaryin, openhook=fileinput.hook_encoded("utf-8")
    ) as fin:
        for line in fin:
            fout.write(line)

    return diaryout
