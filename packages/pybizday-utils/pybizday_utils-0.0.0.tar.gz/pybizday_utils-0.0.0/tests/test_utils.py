import datetime
from typing import Any

import pytest

from pybizday_utils.utils import validate_date_type


@pytest.mark.parametrize(
    "date",
    [
        datetime.date(2025, 1, 1),
        datetime.datetime(2025, 1, 1),
        datetime.datetime(2025, 1, 1, 12, 0),
    ],
)
def test_validate_date_type_with_valid_types(
    date: datetime.date | datetime.datetime,
) -> None:
    """Test validate_date_type with valid date types."""
    assert validate_date_type(date) is True


@pytest.mark.parametrize(
    "invalid_date",
    [
        "2025-01-01",  # string
        20250101,  # integer
        1.5,  # float
        None,  # None
        [],  # list
        {},  # dict
        (2025, 1, 1),  # tuple
    ],
)
def test_validate_date_type_with_invalid_types(invalid_date: Any) -> None:
    """Test validate_date_type with invalid date types."""
    with pytest.raises(TypeError) as exc_info:
        validate_date_type(invalid_date)
    assert "must be a datetime.date or datetime.datetime object" in str(exc_info.value)  # noqa: E501
    assert str(type(invalid_date)) in str(exc_info.value)
