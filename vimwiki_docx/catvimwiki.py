"""Concatenate Vimwiki diary files."""

import datetime
import fileinput
import os
import re
from pathlib import Path
from typing import Tuple

# from dateutil import parser
from dateutil.relativedelta import MO, TH, relativedelta


def get_last_thursday(today: datetime.date = datetime.datetime.now()) -> datetime.date:
    """Return datetime for closest Thursday before today.

    Parameters
    ----------
    today : any date object

    Returns
    -------
    Previous Thursday before today, unless today is Thursday.

    """
    return today + relativedelta(weekday=TH(-1))


def get_last_monday(today: datetime.date = datetime.datetime.now()) -> datetime.date:
    """Return datetime for closest Monday before today.

    Parameters
    ----------
    today : any date object

    Returns
    -------
    Previous Monday before today, unless today is Monday.

    """
    return today + relativedelta(weekday=MO(-1))


# def getdates(
#     start: Union[str, datetime.date] = None,
#     end: Union[str, datetime.date] = None,
# ) -> Tuple[datetime.date, datetime.date]:
#     """TODO: Docstring for getdates.

#     Parameters
#     ----------
#     start :

#     Returns
#     -------
#     startdate : Default to Monday of this week.

#     """
#     enddate: datetime.date
#     if end is None:
#         enddate = datetime.date.today()
#     elif isinstance(end, str):
#         enddate = parser.parse(end)
#     elif isinstance(end, datetime.date):
#         enddate = end
#     else:
#         enddate = None

#     startdate: datetime.date
#     if start is None:
#         startdate = enddate
#     elif
#         startdate = enddate - datetime.timedelta(days=enddate.weekday())

#     return startdate, enddate


def catdiary(
    startdate: datetime.date,
    enddate: datetime.date,
    wikidiary: Path = Path.home() / "Documents/vimwiki/diary",
    refilter: Tuple[str, ...] = (
        # Regex vimwiki tags.
        r"^:.*:$",
        # Regex task [ ]
        r"\s\[\s\]",
        # Regex bullet *
        r"^\s{0,}\*\s",
    ),
):
    """TODO: Docstring for catdiary.

    Parameters
    ----------
    function : TODO

    Returns
    -------
    TODO

    """
    diaryin = wikidiary.glob("[0-9]*.wiki")
    diaryin = (
        day
        for day in diaryin
        if startdate <= datetime.date.fromisoformat(day.stem) <= enddate
    )

    tmppath: str = os.getenv("TMP", os.getcwd())
    diaryout: Path = Path(tmppath) / "prepm.wiki"

    pattern = re.compile(r"|".join(refilter))

    with open(diaryout, "w", encoding="utf8") as fout, fileinput.input(
        diaryin, openhook=fileinput.hook_encoded("utf-8")
    ) as fin:
        for line in fin:
            if re.search(pattern, line) is None:
                fout.write(line)

    return diaryout
