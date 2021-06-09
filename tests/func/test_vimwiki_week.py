"""Test concatenate_diary."""

import datetime
from pathlib import Path

import pytest

from vimwiki_docx.vimwiki_week import concatenate_diary


@pytest.mark.freeze_time("2017-04-27")
@pytest.mark.parametrize(
    "start_date, end_date, expected",
    [
        pytest.param(None, None, (2, 2334), id="No start or end date"),
        pytest.param(
            "2017-04-24", "2017-04-26", (2, 2334), id="Specify start and end dates"
        ),
    ],
)
def test_concatenate_diary(start_date, end_date, expected):
    """Test concatenate_diary with no dates provided.

    Given no start or end dates, concatenate_diary will find 2 diary files,
    return diary path for concatenated size of 2334.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    assert datetime.date.today() == datetime.date(2017, 4, 27)

    diary_path: Path = Path(__file__).parents[0] / "vimwiki/diary"
    assert len(list(diary_path.glob("*.wiki"))) == expected[0]

    diaryout: Path = concatenate_diary(
        diary_path, start_date=start_date, end_date=end_date
    )
    assert diaryout.stat().st_size == expected[1]
