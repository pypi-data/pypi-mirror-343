import datetime
from typing import Callable

import pytest

from pybizday_utils.date_range_utils import date_range


@pytest.mark.positive
@pytest.mark.parametrize(
    "start, end, include_start, include_end, step_days, expected",
    [
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 3),
            True,
            True,
            1,
            [
                datetime.date(2021, 1, 1),
                datetime.date(2021, 1, 2),
                datetime.date(2021, 1, 3),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 3),
            True,
            False,
            1,
            [
                datetime.date(2021, 1, 1),
                datetime.date(2021, 1, 2),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 3),
            False,
            True,
            1,
            [
                datetime.date(2021, 1, 2),
                datetime.date(2021, 1, 3),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 3),
            False,
            False,
            1,
            [
                datetime.date(2021, 1, 2),
            ],
        ),
        (
            datetime.date(2021, 1, 3),
            datetime.date(2021, 1, 1),
            True,
            True,
            -1,
            [
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 2),
                datetime.date(2021, 1, 1),
            ],
        ),
        (
            datetime.date(2021, 1, 3),
            datetime.date(2021, 1, 1),
            True,
            False,
            -1,
            [
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 2),
            ],
        ),
        (
            datetime.date(2021, 1, 3),
            datetime.date(2021, 1, 1),
            False,
            True,
            -1,
            [
                datetime.date(2021, 1, 2),
                datetime.date(2021, 1, 1),
            ],
        ),
        (
            datetime.date(2021, 1, 3),
            datetime.date(2021, 1, 1),
            False,
            False,
            -1,
            [
                datetime.date(2021, 1, 2),
            ],
        ),
    ],
)
def test_date_range_with_end(
    start: datetime.date,
    end: datetime.date,
    include_start: bool,
    include_end: bool,
    step_days: int,
    expected: list[datetime.date],
) -> None:
    actual = list(
        date_range(
            start,
            end,
            include_start=include_start,
            include_end=include_end,
            step_days=step_days,
        )
    )
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "start, include_start, include_end, step_days, expected",
    [
        (
            datetime.date.max - datetime.timedelta(days=3),
            True,
            True,
            1,
            [
                datetime.date.max - datetime.timedelta(days=3),
                datetime.date.max - datetime.timedelta(days=2),
                datetime.date.max - datetime.timedelta(days=1),
                datetime.date.max,
            ],
        ),
        (
            datetime.date.max - datetime.timedelta(days=3),
            True,
            False,
            1,
            [
                datetime.date.max - datetime.timedelta(days=3),
                datetime.date.max - datetime.timedelta(days=2),
                datetime.date.max - datetime.timedelta(days=1),
            ],
        ),
        (
            datetime.date.max - datetime.timedelta(days=3),
            False,
            True,
            1,
            [
                datetime.date.max - datetime.timedelta(days=2),
                datetime.date.max - datetime.timedelta(days=1),
                datetime.date.max,
            ],
        ),
        (
            datetime.date.max - datetime.timedelta(days=3),
            False,
            False,
            1,
            [
                datetime.date.max - datetime.timedelta(days=2),
                datetime.date.max - datetime.timedelta(days=1),
            ],
        ),
        (
            datetime.date.min + datetime.timedelta(days=3),
            True,
            True,
            -1,
            [
                datetime.date.min + datetime.timedelta(days=3),
                datetime.date.min + datetime.timedelta(days=2),
                datetime.date.min + datetime.timedelta(days=1),
                datetime.date.min,
            ],
        ),
        (
            datetime.date.min + datetime.timedelta(days=3),
            True,
            False,
            -1,
            [
                datetime.date.min + datetime.timedelta(days=3),
                datetime.date.min + datetime.timedelta(days=2),
                datetime.date.min + datetime.timedelta(days=1),
            ],
        ),
        (
            datetime.date.min + datetime.timedelta(days=3),
            False,
            True,
            -1,
            [
                datetime.date.min + datetime.timedelta(days=2),
                datetime.date.min + datetime.timedelta(days=1),
                datetime.date.min,
            ],
        ),
        (
            datetime.date.min + datetime.timedelta(days=3),
            False,
            False,
            -1,
            [
                datetime.date.min + datetime.timedelta(days=2),
                datetime.date.min + datetime.timedelta(days=1),
            ],
        ),
    ],
)
def test_date_range_without_end(
    start: datetime.date,
    include_start: bool,
    include_end: bool,
    step_days: int,
    expected: list[datetime.date],
) -> None:
    actual = list(
        date_range(
            start,
            include_start=include_start,
            include_end=include_end,
            step_days=step_days,
        )
    )
    assert actual == expected


@pytest.mark.negative
def test_date_range_with_invalid_step_days() -> None:
    with pytest.raises(ValueError):
        list(date_range(datetime.date(2021, 1, 1), step_days=0))


@pytest.mark.positive
@pytest.mark.parametrize(
    "start, end, include_start, include_end, step_days, expected",
    [
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 7),
            True,
            True,
            2,
            [
                datetime.date(2021, 1, 1),
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 5),
                datetime.date(2021, 1, 7),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 7),
            True,
            False,
            2,
            [
                datetime.date(2021, 1, 1),
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 5),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 7),
            False,
            True,
            2,
            [
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 5),
                datetime.date(2021, 1, 7),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 7),
            False,
            False,
            2,
            [
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 5),
            ],
        ),
        (
            datetime.date(2021, 1, 7),
            datetime.date(2021, 1, 1),
            True,
            True,
            -2,
            [
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 5),
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 1),
            ],
        ),
        (
            datetime.date(2021, 1, 7),
            datetime.date(2021, 1, 1),
            True,
            False,
            -2,
            [
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 5),
                datetime.date(2021, 1, 3),
            ],
        ),
        (
            datetime.date(2021, 1, 7),
            datetime.date(2021, 1, 1),
            False,
            True,
            -2,
            [
                datetime.date(2021, 1, 5),
                datetime.date(2021, 1, 3),
                datetime.date(2021, 1, 1),
            ],
        ),
        (
            datetime.date(2021, 1, 7),
            datetime.date(2021, 1, 1),
            False,
            False,
            -2,
            [
                datetime.date(2021, 1, 5),
                datetime.date(2021, 1, 3),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 13),
            True,
            True,
            3,
            [
                datetime.date(2021, 1, 1),
                datetime.date(2021, 1, 4),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 10),
                datetime.date(2021, 1, 13),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 13),
            True,
            False,
            3,
            [
                datetime.date(2021, 1, 1),
                datetime.date(2021, 1, 4),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 10),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 13),
            False,
            True,
            3,
            [
                datetime.date(2021, 1, 4),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 10),
                datetime.date(2021, 1, 13),
            ],
        ),
        (
            datetime.date(2021, 1, 1),
            datetime.date(2021, 1, 13),
            False,
            False,
            3,
            [
                datetime.date(2021, 1, 4),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 10),
            ],
        ),
        (
            datetime.date(2021, 1, 13),
            datetime.date(2021, 1, 1),
            True,
            True,
            -3,
            [
                datetime.date(2021, 1, 13),
                datetime.date(2021, 1, 10),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 4),
                datetime.date(2021, 1, 1),
            ],
        ),
        (
            datetime.date(2021, 1, 13),
            datetime.date(2021, 1, 1),
            True,
            False,
            -3,
            [
                datetime.date(2021, 1, 13),
                datetime.date(2021, 1, 10),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 4),
            ],
        ),
        (
            datetime.date(2021, 1, 13),
            datetime.date(2021, 1, 1),
            False,
            True,
            -3,
            [
                datetime.date(2021, 1, 10),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 4),
                datetime.date(2021, 1, 1),
            ],
        ),
        (
            datetime.date(2021, 1, 13),
            datetime.date(2021, 1, 1),
            False,
            False,
            -3,
            [
                datetime.date(2021, 1, 10),
                datetime.date(2021, 1, 7),
                datetime.date(2021, 1, 4),
            ],
        ),
    ],
)
def test_date_range_with_not_1_step_days(
    start: datetime.date,
    end: datetime.date,
    include_start: bool,
    include_end: bool,
    step_days: int,
    expected: list[datetime.date],
) -> None:
    actual = list(
        date_range(
            start,
            end,
            include_start=include_start,
            include_end=include_end,
            step_days=step_days,
        )
    )
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "start, end, include_start, include_end, step_days, handler",
    [
        (
            datetime.datetime(2021, 1, 1, 12, 0),
            datetime.datetime(2021, 1, 3, 12, 0),
            True,
            True,
            1,
            lambda dt: dt.date(),
        ),
        (
            datetime.datetime(2021, 1, 1, 12, 0),
            datetime.datetime(2021, 1, 3, 12, 0),
            True,
            False,
            1,
            lambda dt: dt.date(),
        ),
        (
            datetime.datetime(2021, 1, 1, 0, 0),
            datetime.datetime(2021, 1, 3, 0, 0),
            False,
            True,
            1,
            lambda dt: (dt + datetime.timedelta(days=10)).date(),
        ),
    ],
)
def test_date_range_with_datetime_should_return_the_same_result_of_date_range_with_handled_object(  # noqa: E501
    start: datetime.datetime,
    end: datetime.datetime,
    include_start: bool,
    include_end: bool,
    step_days: int,
    handler: Callable[[datetime.datetime], datetime.date],
) -> None:
    handled_start = handler(start)
    handled_end = handler(end)
    actual = list(
        date_range(
            start,
            end,
            include_start=include_start,
            include_end=include_end,
            step_days=step_days,
            datetime_handler=handler,
        )
    )
    expected = list(
        date_range(
            handled_start,
            handled_end,
            include_start=include_start,
            include_end=include_end,
            step_days=step_days,
        )
    )
    assert actual == expected
