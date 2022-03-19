"""Test concatenate_diary."""

import datetime
from pathlib import Path

import pytest

from panvimwiki.vimwiki_week import concatenate_diary

diary_path: Path = Path(__file__).parents[0] / "vimwiki/diary"


@pytest.mark.freeze_time("2017-04-27")
@pytest.mark.parametrize(
    "start_date, end_date, diary_path, expected",
    [
        pytest.param(None, None, diary_path, (2, 2521), id="No start or end date"),
        pytest.param(
            "2017-04-24",
            "2017-04-26",
            diary_path,
            (2, 2521),
            id="Specify start and end dates",
        ),
    ],
)
def test_concatenate_diary(start_date, end_date, diary_path, expected):
    """Test concatenate_diary with no dates provided.

    Given no start or end dates, concatenate_diary will find 2 diary files,
    return diary path for concatenated size of 2334.

    """
    assert datetime.date.today() == datetime.date(2017, 4, 27)

    assert len(list(diary_path.glob("*.wiki"))) == expected[0]

    diaryout: Path = concatenate_diary(
        diary_path, start_date=start_date, end_date=end_date
    )
    assert diaryout.stat().st_size == expected[1]


@pytest.mark.freeze_time("2017-04-27")
@pytest.mark.parametrize(
    "start_date, end_date, diary_path, expected",
    [
        pytest.param(
            None,
            None,
            Path(""),
            (
                OSError,
                "Diary not found at wikidiary=PosixPath('.')",
            ),
            id="Empty diary_path",
        ),
        pytest.param(
            None,
            None,
            None,
            (
                ValueError,
                "diary_path=None. A valid diary path is required.",
            ),
            id="None diary_path",
        ),
    ],
)
def test_concatenate_diary_path(start_date, end_date, diary_path, expected):
    """Test concatenate_diary with no dates provided.

    Given diary_path without *.wiki, concatenate_diary raises OSError.

    Given diary_path=None, concatenate_diary raises ValueError.

    """
    with pytest.raises(expected[0]) as excinfo:
        concatenate_diary(diary_path, start_date=start_date, end_date=end_date)
    assert expected[1] in str(excinfo.value)
