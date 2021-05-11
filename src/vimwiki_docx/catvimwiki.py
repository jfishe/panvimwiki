"""Concatenate Vimwiki diary files."""

import datetime
import fileinput
import os
import re
from pathlib import Path
from typing import Tuple

# from dateutil import parser
from dateutil.relativedelta import MO, TH, relativedelta


def get_last_thursday(today: datetime.date = datetime.date.today()) -> datetime.date:
    """Return datetime for closest Thursday before today.

    Parameters
    ----------
    today : any date object

    Returns
    -------
    Previous Thursday before today, unless today is Thursday.

    """
    return today + relativedelta(weekday=TH(-1))


def get_last_monday(today: datetime.date = datetime.date.today()) -> datetime.date:
    """Return datetime for closest Monday before today.

    Parameters
    ----------
    today : any date object

    Returns
    -------
    Previous Monday before today, unless today is Monday.

    """
    return today + relativedelta(weekday=MO(-1))


def catdiary(
    startdate: datetime.date,
    enddate: datetime.date,
    wikidiary: Path = Path.home() / "vimwiki/diary",
    refilter: Tuple[str, ...] = (
        # Regex vimwiki tags.
        r"^:.*:$",
        # Regex task [ ]
        r"\s\[\s\]",
        # Regex bullet *
        r"^\s{0,}\*\s((?!\[\S\]\s).)*$",
    ),
) -> Path:
    """Concatenate Vimwiki diary files and apply regex filter.

    Parameters
    ----------
    startdate : Starting date for Vimwiki diary entry.

    enddate : End date date for Vimwiki diary entry.

    wikidiary : Path to Vimwiki diary directory. Defaults to
                `$HOME/vimwiki/diary`.

    refilter : Regex to remove matching lines from Vimwiki diary entries.
               Defaults to removing:

               - Vimwiki tag lines, e.g., :tag1:tag2:
               - Not started tasks, e.g., - [ ] Task1
               - Non-task * bullet lines, e.g., * [[URI|Description]] or * Text

    Returns
    -------
    Path to concatenated Vimwiki diary entries from startdate to enddate,
    inclusive of both.

    Raises
    ______
    ValueError
        If `startdate` is after `enddate`

    """
    if startdate > enddate:
        errmsg = f"enddate {enddate} should not precede startdate {startdate}."
        raise ValueError(errmsg)

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


def del_empty_heading(
    wikifile: Path,
    reheading: str = (
        # Match start of line with one or more heading delimeters.
        # Group 1 captures the number of heading delimeters.
        r"^(=+)"
        # Match any characters until Group 1 repeats--i.e., end of heading.
        r".+\1"
        # Match one or more whitespaces, such as EOL.
        r"\s+"
        # Capture Group 2--the beginning of the next heading at the same level
        # or the end of file/string.  Do not match a child heading.
        r"((\1[^=])|\Z)"
    ),
):
    """Remove empty headings from Vimwiki file.

    Apply Regex until no empty headings remain.

    Parameters
    ----------
    wikifile : Path to Vimwiki to modify.

    reheading : Regex to match empty headings. Substitute the regex with
                capture group 2.

    Returns
    -------
    Path to modified Vimikwik file.

    """
    with open(wikifile, "r", encoding="utf8") as fin:
        diary = fin.read()

    pattern = re.compile(reheading, re.MULTILINE)

    def remove_empty_heading(match: re.Match) -> str:
        """Remove empty heading by returning capture group 2 only."""
        return match.group(2)

    ismatch = False
    while re.search(pattern, diary):
        ismatch = True
        diary = re.sub(pattern, remove_empty_heading, diary)

    if ismatch:
        with open(wikifile, "w", encoding="utf8") as fout:
            fout.write(diary)

    return wikifile


def del_taskwiki_heading(
    wikifile: Path,
    reheading: str = (
        # Match start of line with one or more heading delimeters.
        # Group 1 captures the number of heading delimeters.
        r"^(=+)"
        # Match any characters, except pipe, the taskwiki delimeter.
        # Group 2 captures the heading we're keeping.
        r"([^|]+)"
        # Match space pipe, which starts taskwiki heading.
        r"\s\|.+"
        # Match space followed by Group 1.
        r"\s\1$"
    ),
):
    """Remove taskwiki heading.

    wikifile : Path to Vimwiki to modify.

    reheading : Regex to match empty headings. Substitute the regex with
                capture group 2.

    Returns
    -------
    Path to modified Vimikwik file.

    """
    with open(wikifile, "r", encoding="utf8") as fin:
        diary = fin.read()

    pattern = re.compile(reheading, re.MULTILINE)
    replace = r"\1\2 \1"

    if re.search(pattern, diary):
        diary = re.sub(pattern, replace, diary)

        with open(wikifile, "w", encoding="utf8") as fout:
            fout.write(diary)

    return wikifile
