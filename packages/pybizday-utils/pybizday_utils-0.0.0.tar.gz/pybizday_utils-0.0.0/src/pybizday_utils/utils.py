import datetime
from typing import Any, TypeGuard


def validate_date_type(date: Any) -> TypeGuard[datetime.date | datetime.datetime]:
    """Validate that the input is either a datetime.date or datetime.datetime object.

    Args:
        date (Any): The value to validate.

    Returns:
        TypeGuard[datetime.date | datetime.datetime]: True for valid date types.

    Raises:
        TypeError: If the input is not a datetime.date or datetime.datetime object.
    """
    if not isinstance(date, (datetime.date, datetime.datetime)):
        raise TypeError(
            f"date must be a datetime.date or datetime.datetime object, "
            f"not {type(date)}"
        )
    return True
