from datetime import date, datetime, timedelta
from typing import Callable

import pytest
from pytest_mock import MockerFixture

import pybizday_utils.month
from pybizday_utils.month import (
    add_months,
    add_years,
    add_years_months,
    get_biz_end_of_month,
    get_biz_start_of_month,
    is_biz_end_of_month,
    is_biz_start_of_month,
)


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,expected",
    [
        # Case: everyday is not holiday
        (date(2023, 1, 31), lambda _: False, True),
        (date(2023, 2, 28), lambda _: False, True),
        (date(2023, 3, 31), lambda _: False, True),
        (date(2023, 4, 30), lambda _: False, True),
        (date(2023, 5, 31), lambda _: False, True),
        (date(2023, 6, 30), lambda _: False, True),
        (date(2023, 7, 31), lambda _: False, True),
        (date(2023, 8, 31), lambda _: False, True),
        (date(2023, 9, 30), lambda _: False, True),
        (date(2023, 10, 31), lambda _: False, True),
        (date(2023, 11, 30), lambda _: False, True),
        (date(2023, 12, 31), lambda _: False, True),
        (date(2023, 1, 30), lambda _: False, False),
        (date(2023, 2, 27), lambda _: False, False),
        (date(2023, 3, 30), lambda _: False, False),
        (date(2023, 4, 29), lambda _: False, False),
        (date(2023, 5, 30), lambda _: False, False),
        (date(2023, 6, 29), lambda _: False, False),
        (date(2023, 7, 30), lambda _: False, False),
        (date(2023, 8, 30), lambda _: False, False),
        (date(2023, 9, 29), lambda _: False, False),
        (date(2023, 10, 30), lambda _: False, False),
        (date(2023, 11, 29), lambda _: False, False),
        (date(2023, 12, 30), lambda _: False, False),
        # Case: specify is_holiday function
        (date(2023, 1, 31), lambda d: d == date(2023, 1, 31), False),
        (date(2023, 1, 30), lambda d: d == date(2023, 1, 31), True),
        (date(2023, 1, 29), lambda d: d == date(2023, 1, 31), False),
        (date(2023, 2, 28), lambda d: d == date(2023, 2, 28), False),
        (date(2023, 2, 27), lambda d: d == date(2023, 2, 28), True),
        (date(2023, 2, 26), lambda d: d == date(2023, 2, 28), False),
        (date(2023, 3, 31), lambda d: d == date(2023, 3, 31), False),
        (date(2023, 3, 30), lambda d: d == date(2023, 3, 31), True),
        (date(2023, 3, 29), lambda d: d == date(2023, 3, 31), False),
        (date(2023, 4, 30), lambda d: d == date(2023, 4, 30), False),
        (date(2023, 4, 29), lambda d: d == date(2023, 4, 30), True),
        (date(2023, 4, 28), lambda d: d == date(2023, 4, 30), False),
        (date(2023, 5, 31), lambda d: d == date(2023, 5, 31), False),
        (date(2023, 5, 30), lambda d: d == date(2023, 5, 31), True),
        (date(2023, 5, 29), lambda d: d == date(2023, 5, 31), False),
        (date(2023, 6, 30), lambda d: d == date(2023, 6, 30), False),
        (date(2023, 6, 29), lambda d: d == date(2023, 6, 30), True),
        (date(2023, 6, 28), lambda d: d == date(2023, 6, 30), False),
        (date(2023, 7, 31), lambda d: d == date(2023, 7, 31), False),
        (date(2023, 7, 30), lambda d: d == date(2023, 7, 31), True),
        (date(2023, 7, 29), lambda d: d == date(2023, 7, 31), False),
        (date(2023, 8, 31), lambda d: d == date(2023, 8, 31), False),
        (date(2023, 8, 30), lambda d: d == date(2023, 8, 31), True),
        (date(2023, 8, 29), lambda d: d == date(2023, 8, 31), False),
        (date(2023, 9, 30), lambda d: d == date(2023, 9, 30), False),
        (date(2023, 9, 29), lambda d: d == date(2023, 9, 30), True),
        (date(2023, 9, 28), lambda d: d == date(2023, 9, 30), False),
        (date(2023, 10, 31), lambda d: d == date(2023, 10, 31), False),
        (date(2023, 10, 30), lambda d: d == date(2023, 10, 31), True),
        (date(2023, 10, 29), lambda d: d == date(2023, 10, 31), False),
        (date(2023, 11, 30), lambda d: d == date(2023, 11, 30), False),
        (date(2023, 11, 29), lambda d: d == date(2023, 11, 30), True),
        (date(2023, 11, 28), lambda d: d == date(2023, 11, 30), False),
        (date(2023, 12, 31), lambda d: d == date(2023, 12, 31), False),
        (date(2023, 12, 30), lambda d: d == date(2023, 12, 31), True),
        (date(2023, 12, 29), lambda d: d == date(2023, 12, 31), False),
        # Case: actual. Saturday and Sunday are holidays
        (date(2024, 11, 30), lambda d: d.weekday() in {5, 6}, False),
        (date(2024, 11, 29), lambda d: d.weekday() in {5, 6}, True),
        (date(2024, 11, 28), lambda d: d.weekday() in {5, 6}, False),
        (date(2025, 1, 31), lambda d: d.weekday() in {5, 6}, True),
        (date(2025, 1, 30), lambda d: d.weekday() in {5, 6}, False),
    ],
)
def test_is_biz_end_of_month(
    d: date,
    is_holiday: Callable[[date], bool],
    expected: bool,
) -> None:
    assert is_biz_end_of_month(d, is_holiday) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,expected",
    [
        # Case: everyday is not holiday
        (date(2023, 1, 1), lambda _: False, True),
        (date(2023, 2, 1), lambda _: False, True),
        (date(2023, 3, 1), lambda _: False, True),
        (date(2023, 4, 1), lambda _: False, True),
        (date(2023, 5, 1), lambda _: False, True),
        (date(2023, 6, 1), lambda _: False, True),
        (date(2023, 7, 1), lambda _: False, True),
        (date(2023, 8, 1), lambda _: False, True),
        (date(2023, 9, 1), lambda _: False, True),
        (date(2023, 10, 1), lambda _: False, True),
        (date(2023, 11, 1), lambda _: False, True),
        (date(2023, 12, 1), lambda _: False, True),
        (date(2023, 1, 2), lambda _: False, False),
        (date(2023, 2, 2), lambda _: False, False),
        (date(2023, 3, 2), lambda _: False, False),
        (date(2023, 4, 2), lambda _: False, False),
        (date(2023, 5, 2), lambda _: False, False),
        (date(2023, 6, 2), lambda _: False, False),
        (date(2023, 7, 2), lambda _: False, False),
        (date(2023, 8, 2), lambda _: False, False),
        (date(2023, 9, 2), lambda _: False, False),
        (date(2023, 10, 2), lambda _: False, False),
        (date(2023, 11, 2), lambda _: False, False),
        (date(2023, 12, 2), lambda _: False, False),
        # Case: specify is_holiday function
        (date(2023, 1, 1), lambda d: d == date(2023, 1, 1), False),
        (date(2023, 1, 2), lambda d: d == date(2023, 1, 1), True),
        (date(2023, 1, 3), lambda d: d == date(2023, 1, 1), False),
        (date(2023, 2, 1), lambda d: d == date(2023, 2, 1), False),
        (date(2023, 2, 2), lambda d: d == date(2023, 2, 1), True),
        (date(2023, 2, 3), lambda d: d == date(2023, 2, 1), False),
        (date(2023, 3, 1), lambda d: d == date(2023, 3, 1), False),
        (date(2023, 3, 2), lambda d: d == date(2023, 3, 1), True),
        (date(2023, 3, 3), lambda d: d == date(2023, 3, 1), False),
        (date(2023, 4, 1), lambda d: d == date(2023, 4, 1), False),
        (date(2023, 4, 2), lambda d: d == date(2023, 4, 1), True),
        (date(2023, 4, 3), lambda d: d == date(2023, 4, 1), False),
        (date(2023, 5, 1), lambda d: d == date(2023, 5, 1), False),
        (date(2023, 5, 2), lambda d: d == date(2023, 5, 1), True),
        (date(2023, 5, 3), lambda d: d == date(2023, 5, 1), False),
        (date(2023, 6, 1), lambda d: d == date(2023, 6, 1), False),
        (date(2023, 6, 2), lambda d: d == date(2023, 6, 1), True),
        (date(2023, 6, 3), lambda d: d == date(2023, 6, 1), False),
        (date(2023, 7, 1), lambda d: d == date(2023, 7, 1), False),
        (date(2023, 7, 2), lambda d: d == date(2023, 7, 1), True),
        (date(2023, 7, 3), lambda d: d == date(2023, 7, 1), False),
        (date(2023, 8, 1), lambda d: d == date(2023, 8, 1), False),
        (date(2023, 8, 2), lambda d: d == date(2023, 8, 1), True),
        (date(2023, 8, 3), lambda d: d == date(2023, 8, 1), False),
        (date(2023, 9, 1), lambda d: d == date(2023, 9, 1), False),
        (date(2023, 9, 2), lambda d: d == date(2023, 9, 1), True),
        (date(2023, 9, 3), lambda d: d == date(2023, 9, 1), False),
        (date(2023, 10, 1), lambda d: d == date(2023, 10, 1), False),
        (date(2023, 10, 2), lambda d: d == date(2023, 10, 1), True),
        (date(2023, 10, 3), lambda d: d == date(2023, 10, 1), False),
        (date(2023, 11, 1), lambda d: d == date(2023, 11, 1), False),
        (date(2023, 11, 2), lambda d: d == date(2023, 11, 1), True),
        (date(2023, 11, 3), lambda d: d == date(2023, 11, 1), False),
        (date(2023, 12, 1), lambda d: d == date(2023, 12, 1), False),
        (date(2023, 12, 2), lambda d: d == date(2023, 12, 1), True),
        (date(2023, 12, 3), lambda d: d == date(2023, 12, 1), False),
        # Case: actual. Saturday and Sunday are holidays
        (date(2024, 12, 1), lambda d: d.weekday() in {5, 6}, False),
        (date(2024, 12, 2), lambda d: d.weekday() in {5, 6}, True),
        (date(2024, 12, 3), lambda d: d.weekday() in {5, 6}, False),
        (date(2024, 11, 1), lambda d: d.weekday() in {5, 6}, True),
        (date(2024, 11, 2), lambda d: d.weekday() in {5, 6}, False),
    ],
)
def test_is_biz_start_of_month(
    d: date,
    is_holiday: Callable[[date], bool],
    expected: bool,
) -> None:
    assert is_biz_start_of_month(d, is_holiday) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,expected",
    [
        # Case: everyday is not holiday
        (date(2023, 1, 1), lambda _: False, date(2023, 1, 1)),
        (date(2023, 1, 31), lambda _: False, date(2023, 1, 1)),
        (date(2023, 2, 1), lambda _: False, date(2023, 2, 1)),
        (date(2023, 2, 28), lambda _: False, date(2023, 2, 1)),
        (date(2023, 3, 1), lambda _: False, date(2023, 3, 1)),
        (date(2023, 3, 31), lambda _: False, date(2023, 3, 1)),
        (date(2023, 4, 1), lambda _: False, date(2023, 4, 1)),
        (date(2023, 4, 30), lambda _: False, date(2023, 4, 1)),
        (date(2023, 5, 1), lambda _: False, date(2023, 5, 1)),
        (date(2023, 5, 31), lambda _: False, date(2023, 5, 1)),
        (date(2023, 6, 1), lambda _: False, date(2023, 6, 1)),
        (date(2023, 6, 30), lambda _: False, date(2023, 6, 1)),
        (date(2023, 7, 1), lambda _: False, date(2023, 7, 1)),
        (date(2023, 7, 31), lambda _: False, date(2023, 7, 1)),
        (date(2023, 8, 1), lambda _: False, date(2023, 8, 1)),
        (date(2023, 8, 31), lambda _: False, date(2023, 8, 1)),
        (date(2023, 9, 1), lambda _: False, date(2023, 9, 1)),
        (date(2023, 9, 30), lambda _: False, date(2023, 9, 1)),
        (date(2023, 10, 1), lambda _: False, date(2023, 10, 1)),
        (date(2023, 10, 31), lambda _: False, date(2023, 10, 1)),
        (date(2023, 11, 1), lambda _: False, date(2023, 11, 1)),
        (date(2023, 11, 30), lambda _: False, date(2023, 11, 1)),
        (date(2023, 12, 1), lambda _: False, date(2023, 12, 1)),
        (date(2023, 12, 31), lambda _: False, date(2023, 12, 1)),
        # Case: specify is_holiday function
        (date(2023, 1, 1), lambda d: d == date(2023, 1, 1), date(2023, 1, 2)),
        (date(2023, 1, 2), lambda d: d == date(2023, 1, 1), date(2023, 1, 2)),
        (date(2023, 1, 31), lambda d: d == date(2023, 1, 1), date(2023, 1, 2)),
        (date(2023, 2, 1), lambda d: d == date(2023, 2, 1), date(2023, 2, 2)),
        (date(2023, 2, 2), lambda d: d == date(2023, 2, 1), date(2023, 2, 2)),
        (date(2023, 2, 28), lambda d: d == date(2023, 2, 1), date(2023, 2, 2)),
        (date(2023, 3, 1), lambda d: d == date(2023, 3, 1), date(2023, 3, 2)),
        (date(2023, 3, 2), lambda d: d == date(2023, 3, 1), date(2023, 3, 2)),
        (date(2023, 3, 31), lambda d: d == date(2023, 3, 1), date(2023, 3, 2)),
        (date(2023, 4, 1), lambda d: d == date(2023, 4, 1), date(2023, 4, 2)),
        (date(2023, 4, 2), lambda d: d == date(2023, 4, 1), date(2023, 4, 2)),
        (date(2023, 4, 30), lambda d: d == date(2023, 4, 1), date(2023, 4, 2)),
        (date(2023, 5, 1), lambda d: d == date(2023, 5, 1), date(2023, 5, 2)),
        (date(2023, 5, 2), lambda d: d == date(2023, 5, 1), date(2023, 5, 2)),
        (date(2023, 5, 31), lambda d: d == date(2023, 5, 1), date(2023, 5, 2)),
        (date(2023, 6, 1), lambda d: d == date(2023, 6, 1), date(2023, 6, 2)),
        (date(2023, 6, 2), lambda d: d == date(2023, 6, 1), date(2023, 6, 2)),
        (date(2023, 6, 30), lambda d: d == date(2023, 6, 1), date(2023, 6, 2)),
        (date(2023, 7, 1), lambda d: d == date(2023, 7, 1), date(2023, 7, 2)),
        (date(2023, 7, 2), lambda d: d == date(2023, 7, 1), date(2023, 7, 2)),
        (date(2023, 7, 31), lambda d: d == date(2023, 7, 1), date(2023, 7, 2)),
        (date(2023, 8, 1), lambda d: d == date(2023, 8, 1), date(2023, 8, 2)),
        (date(2023, 8, 2), lambda d: d == date(2023, 8, 1), date(2023, 8, 2)),
        (date(2023, 8, 31), lambda d: d == date(2023, 8, 1), date(2023, 8, 2)),
        (date(2023, 9, 1), lambda d: d == date(2023, 9, 1), date(2023, 9, 2)),
        (date(2023, 9, 2), lambda d: d == date(2023, 9, 1), date(2023, 9, 2)),
        (date(2023, 9, 30), lambda d: d == date(2023, 9, 1), date(2023, 9, 2)),
        (date(2023, 10, 1), lambda d: d == date(2023, 10, 1), date(2023, 10, 2)),
        (date(2023, 10, 2), lambda d: d == date(2023, 10, 1), date(2023, 10, 2)),
        (date(2023, 10, 31), lambda d: d == date(2023, 10, 1), date(2023, 10, 2)),
        (date(2023, 11, 1), lambda d: d == date(2023, 11, 1), date(2023, 11, 2)),
        (date(2023, 11, 2), lambda d: d == date(2023, 11, 1), date(2023, 11, 2)),
        (date(2023, 11, 30), lambda d: d == date(2023, 11, 1), date(2023, 11, 2)),
        (date(2023, 12, 1), lambda d: d == date(2023, 12, 1), date(2023, 12, 2)),
        (date(2023, 12, 2), lambda d: d == date(2023, 12, 1), date(2023, 12, 2)),
        (date(2023, 12, 31), lambda d: d == date(2023, 12, 1), date(2023, 12, 2)),
    ],
)
def test_get_biz_start_of_month(
    d: date,
    is_holiday: Callable[[date], bool],
    expected: date,
) -> None:
    assert get_biz_start_of_month(d, is_holiday) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,expected",
    [
        # Case: everyday is not holiday
        (date(2023, 1, 1), lambda _: False, date(2023, 1, 31)),
        (date(2023, 1, 31), lambda _: False, date(2023, 1, 31)),
        (date(2023, 2, 1), lambda _: False, date(2023, 2, 28)),
        (date(2023, 2, 28), lambda _: False, date(2023, 2, 28)),
        (date(2023, 3, 1), lambda _: False, date(2023, 3, 31)),
        (date(2023, 3, 31), lambda _: False, date(2023, 3, 31)),
        (date(2023, 4, 1), lambda _: False, date(2023, 4, 30)),
        (date(2023, 4, 30), lambda _: False, date(2023, 4, 30)),
        (date(2023, 5, 1), lambda _: False, date(2023, 5, 31)),
        (date(2023, 5, 31), lambda _: False, date(2023, 5, 31)),
        (date(2023, 6, 1), lambda _: False, date(2023, 6, 30)),
        (date(2023, 6, 30), lambda _: False, date(2023, 6, 30)),
        (date(2023, 7, 1), lambda _: False, date(2023, 7, 31)),
        (date(2023, 7, 31), lambda _: False, date(2023, 7, 31)),
        (date(2023, 8, 1), lambda _: False, date(2023, 8, 31)),
        (date(2023, 8, 31), lambda _: False, date(2023, 8, 31)),
        (date(2023, 9, 1), lambda _: False, date(2023, 9, 30)),
        (date(2023, 9, 30), lambda _: False, date(2023, 9, 30)),
        (date(2023, 10, 1), lambda _: False, date(2023, 10, 31)),
        (date(2023, 10, 31), lambda _: False, date(2023, 10, 31)),
        (date(2023, 11, 1), lambda _: False, date(2023, 11, 30)),
        (date(2023, 11, 30), lambda _: False, date(2023, 11, 30)),
        (date(2023, 12, 1), lambda _: False, date(2023, 12, 31)),
        (date(2023, 12, 31), lambda _: False, date(2023, 12, 31)),
        (date(2024, 2, 1), lambda _: False, date(2024, 2, 29)),
        (date(2024, 2, 29), lambda _: False, date(2024, 2, 29)),
        # Case: specify is_holiday function
        (date(2023, 1, 1), lambda d: d == date(2023, 1, 31), date(2023, 1, 30)),
        (date(2023, 1, 30), lambda d: d == date(2023, 1, 31), date(2023, 1, 30)),
        (date(2023, 1, 31), lambda d: d == date(2023, 1, 31), date(2023, 1, 30)),
        (date(2023, 2, 1), lambda d: d == date(2023, 2, 28), date(2023, 2, 27)),
        (date(2023, 2, 27), lambda d: d == date(2023, 2, 28), date(2023, 2, 27)),
        (date(2023, 2, 28), lambda d: d == date(2023, 2, 28), date(2023, 2, 27)),
        (date(2023, 3, 1), lambda d: d == date(2023, 3, 31), date(2023, 3, 30)),
        (date(2023, 3, 30), lambda d: d == date(2023, 3, 31), date(2023, 3, 30)),
        (date(2023, 3, 31), lambda d: d == date(2023, 3, 31), date(2023, 3, 30)),
        (date(2023, 4, 1), lambda d: d == date(2023, 4, 30), date(2023, 4, 29)),
        (date(2023, 4, 29), lambda d: d == date(2023, 4, 30), date(2023, 4, 29)),
        (date(2023, 4, 30), lambda d: d == date(2023, 4, 30), date(2023, 4, 29)),
        (date(2023, 5, 1), lambda d: d == date(2023, 5, 31), date(2023, 5, 30)),
        (date(2023, 5, 30), lambda d: d == date(2023, 5, 31), date(2023, 5, 30)),
        (date(2023, 5, 31), lambda d: d == date(2023, 5, 31), date(2023, 5, 30)),
        (date(2023, 6, 1), lambda d: d == date(2023, 6, 30), date(2023, 6, 29)),
        (date(2023, 6, 29), lambda d: d == date(2023, 6, 30), date(2023, 6, 29)),
        (date(2023, 6, 30), lambda d: d == date(2023, 6, 30), date(2023, 6, 29)),
        (date(2023, 7, 1), lambda d: d == date(2023, 7, 31), date(2023, 7, 30)),
        (date(2023, 7, 30), lambda d: d == date(2023, 7, 31), date(2023, 7, 30)),
        (date(2023, 7, 31), lambda d: d == date(2023, 7, 31), date(2023, 7, 30)),
        (date(2023, 8, 1), lambda d: d == date(2023, 8, 31), date(2023, 8, 30)),
        (date(2023, 8, 30), lambda d: d == date(2023, 8, 31), date(2023, 8, 30)),
        (date(2023, 8, 31), lambda d: d == date(2023, 8, 31), date(2023, 8, 30)),
        (date(2023, 9, 1), lambda d: d == date(2023, 9, 30), date(2023, 9, 29)),
        (date(2023, 9, 29), lambda d: d == date(2023, 9, 30), date(2023, 9, 29)),
        (date(2023, 9, 30), lambda d: d == date(2023, 9, 30), date(2023, 9, 29)),
        (date(2023, 10, 1), lambda d: d == date(2023, 10, 31), date(2023, 10, 30)),
        (date(2023, 10, 30), lambda d: d == date(2023, 10, 31), date(2023, 10, 30)),  # noqa: E501
        (date(2023, 10, 31), lambda d: d == date(2023, 10, 31), date(2023, 10, 30)),  # noqa: E501
        (date(2023, 11, 1), lambda d: d == date(2023, 11, 30), date(2023, 11, 29)),  # noqa: E501
        (date(2023, 11, 29), lambda d: d == date(2023, 11, 30), date(2023, 11, 29)),  # noqa: E501
        (date(2023, 11, 30), lambda d: d == date(2023, 11, 30), date(2023, 11, 29)),  # noqa: E501
        (date(2023, 12, 1), lambda d: d == date(2023, 12, 31), date(2023, 12, 30)),  # noqa: E501
        (date(2023, 12, 30), lambda d: d == date(2023, 12, 31), date(2023, 12, 30)),  # noqa: E501
        (date(2023, 12, 31), lambda d: d == date(2023, 12, 31), date(2023, 12, 30)),  # noqa: E501
    ],
)
def test_get_biz_end_of_month(
    d: date,
    is_holiday: Callable[[date], bool],
    expected: date,
) -> None:
    assert get_biz_end_of_month(d, is_holiday) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,years,months,is_holiday,expected",
    [
        (date(2024, 2, 1), 0, 0, lambda _: False, date(2024, 2, 1)),
        (date(2024, 2, 15), 0, 0, lambda _: False, date(2024, 2, 15)),
        (date(2024, 2, 28), 0, 0, lambda _: False, date(2024, 2, 28)),
        (date(2024, 2, 29), 0, 0, lambda _: False, date(2024, 2, 29)),
        (date(2024, 3, 31), 0, 0, lambda _: False, date(2024, 3, 31)),
        (date(2024, 2, 1), 0, -1, lambda _: False, date(2024, 1, 1)),
        (date(2024, 2, 15), 0, -1, lambda _: False, date(2024, 1, 15)),
        (date(2024, 2, 28), 0, -1, lambda _: False, date(2024, 1, 28)),
        (date(2024, 2, 29), 0, -1, lambda _: False, date(2024, 1, 29)),
        (date(2024, 3, 31), 0, -1, lambda _: False, date(2024, 2, 29)),
        (date(2024, 2, 1), 0, -2, lambda _: False, date(2023, 12, 1)),
        (date(2024, 2, 15), 0, -2, lambda _: False, date(2023, 12, 15)),
        (date(2024, 2, 28), 0, -2, lambda _: False, date(2023, 12, 28)),
        (date(2024, 2, 29), 0, -2, lambda _: False, date(2023, 12, 29)),
        (date(2024, 3, 31), 0, -2, lambda _: False, date(2024, 1, 31)),
    ],
)
def test_add_years_months_with_bizeom2bizeomFalse_bizsom2bizsomFalse(
    d: date,
    years: int,
    months: int,
    is_holiday: Callable[[date], bool],
    expected: date,
) -> None:
    actual = add_years_months(
        d,
        years,
        months,
        is_holiday,
        bizeom2bizeom=False,
        bizsom2bizsom=False,
    )
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,years,months,is_holiday,expected",
    [
        (date(2024, 2, 1), 0, 0, lambda _: False, date(2024, 2, 1)),
        (date(2024, 2, 15), 0, 0, lambda _: False, date(2024, 2, 15)),
        (date(2024, 2, 28), 0, 0, lambda _: False, date(2024, 2, 28)),
        (date(2024, 2, 29), 0, 0, lambda _: False, date(2024, 2, 29)),
        (date(2024, 3, 31), 0, 0, lambda _: False, date(2024, 3, 31)),
        (date(2024, 2, 1), 0, -1, lambda _: False, date(2024, 1, 1)),
        (date(2024, 2, 15), 0, -1, lambda _: False, date(2024, 1, 15)),
        (date(2024, 2, 28), 0, -1, lambda _: False, date(2024, 1, 28)),
        (date(2024, 2, 29), 0, -1, lambda _: False, date(2024, 1, 31)),
        (date(2024, 3, 31), 0, -1, lambda _: False, date(2024, 2, 29)),
        (date(2024, 2, 1), 0, -1, lambda d: d == date(2024, 1, 1), date(2024, 1, 2)),  # noqa: E501
        (date(2024, 2, 15), 0, -1, lambda d: d == date(2024, 1, 15), date(2024, 1, 15)),  # noqa: E501
        (date(2024, 2, 28), 0, -1, lambda d: d == date(2024, 1, 28), date(2024, 1, 28)),  # noqa: E501
        (date(2024, 2, 29), 0, -1, lambda d: d == date(2024, 1, 29), date(2024, 1, 31)),  # noqa: E501
        (date(2024, 3, 31), 0, -1, lambda d: d == date(2024, 2, 29), date(2024, 2, 28)),  # noqa: E501
        (date(2024, 2, 1), 0, 1, lambda _: False, date(2024, 3, 1)),
        (date(2024, 2, 15), 0, 1, lambda _: False, date(2024, 3, 15)),
        (date(2024, 2, 28), 0, 1, lambda _: False, date(2024, 3, 28)),
        (date(2024, 2, 29), 0, 1, lambda _: False, date(2024, 3, 31)),
        (date(2024, 3, 31), 0, 1, lambda _: False, date(2024, 4, 30)),
        (date(2024, 2, 1), 0, 1, lambda d: d == date(2024, 3, 1), date(2024, 3, 2)),  # noqa: E501
        (date(2024, 2, 15), 0, 1, lambda d: d == date(2024, 3, 15), date(2024, 3, 15)),  # noqa: E501
        (date(2024, 2, 28), 0, 1, lambda d: d == date(2024, 3, 28), date(2024, 3, 28)),  # noqa: E501
        (date(2024, 2, 29), 0, 1, lambda d: d == date(2024, 3, 31), date(2024, 3, 30)),  # noqa: E501
        (date(2024, 3, 31), 0, 1, lambda d: d == date(2024, 4, 30), date(2024, 4, 29)),  # noqa: E501
        (date(2024, 2, 1), 1, 0, lambda _: False, date(2025, 2, 1)),
        (date(2024, 2, 15), 1, 0, lambda _: False, date(2025, 2, 15)),
        (date(2024, 2, 28), 1, 0, lambda _: False, date(2025, 2, 28)),
        (date(2024, 2, 29), 1, 0, lambda _: False, date(2025, 2, 28)),
        (date(2024, 3, 31), 1, 0, lambda _: False, date(2025, 3, 31)),
        (date(2024, 2, 1), 1, 0, lambda d: d == date(2025, 2, 1), date(2025, 2, 2)),  # noqa: E501
        (date(2024, 2, 15), 1, 0, lambda d: d == date(2025, 2, 15), date(2025, 2, 15)),  # noqa: E501
        (date(2024, 2, 28), 1, 0, lambda d: d == date(2025, 2, 28), date(2025, 2, 28)),  # noqa: E501
        (date(2024, 2, 29), 1, 0, lambda d: d == date(2025, 2, 28), date(2025, 2, 27)),  # noqa: E501
        (date(2024, 3, 31), 1, 0, lambda d: d == date(2025, 3, 31), date(2025, 3, 30)),  # noqa: E501
        (date(2025, 2, 28), -1, 0, lambda _: False, date(2024, 2, 29)),
    ],
)
def test_add_years_months_with_bizeom2bizeomTrue_bizsom2bizsomTrue(
    d: date,
    years: int,
    months: int,
    is_holiday: Callable[[date], bool],
    expected: date,
) -> None:
    actual = add_years_months(
        d,
        years,
        months,
        is_holiday,
        bizeom2bizeom=True,
        bizsom2bizsom=True,
    )
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "date, months, is_holiday, bizeom2bizeom, bizsom2bizsom",
    [
        (
            date(2023, 1, 1),
            0,
            lambda _: False,
            True,
            True,
        ),
        (
            date(2023, 1, 5),
            -1,
            lambda _: False,
            True,
            False,
        ),
        (
            date(2023, 1, 5),
            -2,
            lambda _: False,
            False,
            True,
        ),
        (
            date(2023, 1, 5),
            -3,
            lambda _: False,
            False,
            False,
        ),
        (
            date(2023, 1, 5),
            1,
            lambda d: d == date(2023, 1, 25),
            True,
            True,
        ),
        (
            date(2023, 1, 5),
            2,
            lambda d: d == date(2023, 1, 25),
            False,
            True,
        ),
        (
            date(2023, 1, 5),
            3,
            lambda d: d == date(2023, 1, 25),
            False,
            False,
        ),
        (
            date(2023, 1, 5),
            4,
            lambda d: d == date(2023, 1, 25),
            True,
            False,
        ),
    ],
)
def test_add_months(
    date: date,
    months: int,
    is_holiday: Callable[[date], bool],
    bizeom2bizeom: bool,
    bizsom2bizsom: bool,
    mocker: MockerFixture,
) -> None:
    # Spy on the add_years_months function to verify its usage
    add_years_months_spy = mocker.spy(pybizday_utils.month, "add_years_months")
    # Call the add_months function
    _ = add_months(
        date,
        months,
        is_holiday,
        bizeom2bizeom=bizeom2bizeom,
        bizsom2bizsom=bizsom2bizsom,
    )
    # Assert
    add_years_months_spy.assert_called_once_with(
        date,
        0,
        months,
        is_holiday,
        bizeom2bizeom=bizeom2bizeom,
        bizsom2bizsom=bizsom2bizsom,
        datetime_handler=datetime.date,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "date, years, is_holiday, bizeom2bizeom, bizsom2bizsom",
    [
        (
            date(2023, 1, 1),
            0,
            lambda _: False,
            True,
            True,
        ),
        (
            date(2023, 1, 5),
            -1,
            lambda _: False,
            True,
            False,
        ),
        (
            date(2023, 1, 5),
            -2,
            lambda _: False,
            False,
            True,
        ),
        (
            date(2023, 1, 5),
            -3,
            lambda _: False,
            False,
            False,
        ),
        (
            date(2023, 1, 5),
            1,
            lambda d: d == date(2023, 1, 25),
            True,
            True,
        ),
        (
            date(2023, 1, 5),
            2,
            lambda d: d == date(2023, 1, 25),
            False,
            True,
        ),
        (
            date(2023, 1, 5),
            3,
            lambda d: d == date(2023, 1, 25),
            False,
            False,
        ),
        (
            date(2023, 1, 5),
            4,
            lambda d: d == date(2023, 1, 25),
            True,
            False,
        ),
    ],
)
def test_add_years(
    date: date,
    years: int,
    is_holiday: Callable[[date], bool],
    bizeom2bizeom: bool,
    bizsom2bizsom: bool,
    mocker: MockerFixture,
) -> None:
    # Spy on the add_years_months function to verify its usage
    add_years_months_spy = mocker.spy(pybizday_utils.month, "add_years_months")
    # Call the add_years function
    _ = add_years(
        date,
        years,
        is_holiday,
        bizeom2bizeom=bizeom2bizeom,
        bizsom2bizsom=bizsom2bizsom,
    )
    # Assert
    add_years_months_spy.assert_called_once_with(
        date,
        years,
        0,
        is_holiday,
        bizeom2bizeom=bizeom2bizeom,
        bizsom2bizsom=bizsom2bizsom,
        datetime_handler=datetime.date,
    )


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,handler",
    [
        (datetime(2023, 1, 1, 12), lambda _: False, datetime.date),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=1)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=2)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=3)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=4)).date(),
        ),
    ],
)
def test_is_biz_end_of_month_with_datetime_obj_should_return_the_same_result_of_is_biz_end_of_month_with_handled_date(  # noqa: E501
    d: datetime,
    is_holiday: Callable[[date], bool],
    handler: Callable[[datetime], date],
) -> None:
    handled = handler(d)
    actual = is_biz_end_of_month(d, is_holiday, datetime_handler=handler)
    expected = is_biz_end_of_month(handled, is_holiday)
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,handler",
    [
        (datetime(2023, 1, 1, 12), lambda _: False, datetime.date),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=1)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=2)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=3)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=4)).date(),
        ),
    ],
)
def test_is_biz_start_of_month_with_datetime_obj_should_return_the_same_result_of_is_biz_start_of_month_with_handled_date(  # noqa: E501
    d: datetime,
    is_holiday: Callable[[date], bool],
    handler: Callable[[datetime], date],
) -> None:
    handled = handler(d)
    actual = is_biz_start_of_month(d, is_holiday, datetime_handler=handler)
    expected = is_biz_start_of_month(handled, is_holiday)
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,handler",
    [
        (datetime(2023, 1, 1, 12), lambda _: False, datetime.date),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=1)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=2)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=3)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=4)).date(),
        ),
    ],
)
def test_get_biz_end_of_month_with_datetime_obj_should_return_the_same_result_of_get_biz_end_of_month_with_handled_date(  # noqa: E501
    d: datetime,
    is_holiday: Callable[[date], bool],
    handler: Callable[[datetime], date],
) -> None:
    handled = handler(d)
    actual = get_biz_end_of_month(d, is_holiday, datetime_handler=handler)
    expected = get_biz_end_of_month(handled, is_holiday)
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,is_holiday,handler",
    [
        (datetime(2023, 1, 1, 12), lambda _: False, datetime.date),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=1)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=2)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=3)).date(),
        ),
        (
            datetime(2023, 1, 1, 12),
            lambda _: False,
            lambda x: (x + timedelta(days=4)).date(),
        ),
    ],
)
def test_get_biz_start_of_month_with_datetime_obj_should_return_the_same_result_of_get_biz_start_of_month_with_handled_date(  # noqa: E501
    d: datetime,
    is_holiday: Callable[[date], bool],
    handler: Callable[[datetime], date],
) -> None:
    handled = handler(d)
    actual = get_biz_start_of_month(d, is_holiday, datetime_handler=handler)
    expected = get_biz_start_of_month(handled, is_holiday)
    assert actual == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d,years,months,is_holiday,handler",
    [
        (datetime(2024, 2, 1, 12), 1, 1, lambda _: False, datetime.date),
        (
            datetime(2024, 2, 15, 12),
            1,
            1,
            lambda _: False,
            lambda x: (x + timedelta(days=1)).date(),
        ),
        (
            datetime(2024, 2, 28, 12),
            1,
            1,
            lambda _: False,
            lambda x: (x + timedelta(days=2)).date(),
        ),
        (
            datetime(2024, 2, 29, 12),
            1,
            1,
            lambda _: False,
            lambda x: (x + timedelta(days=3)).date(),
        ),
        (
            datetime(2024, 3, 31, 12),
            1,
            1,
            lambda _: False,
            lambda x: (x + timedelta(days=4)).date(),
        ),
    ],
)
def test_add_years_months_with_datetime_obj_should_return_the_same_result_of_add_years_months_with_handled_date(  # noqa: E501
    d: datetime,
    years: int,
    months: int,
    is_holiday: Callable[[date], bool],
    handler: Callable[[datetime], date],
) -> None:
    handled = handler(d)
    actual = add_years_months(
        d,
        years,
        months,
        is_holiday,
        datetime_handler=handler,
    )
    expected = add_years_months(handled, years, months, is_holiday)
    assert actual == expected
