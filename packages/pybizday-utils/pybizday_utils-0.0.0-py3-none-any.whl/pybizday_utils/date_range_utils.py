import datetime
from typing import Callable, Generator

from .utils import validate_date_type


def date_range(
    start: datetime.date | datetime.datetime,
    end: datetime.date | datetime.datetime | None = None,
    *,
    include_start: bool = True,
    include_end: bool = True,
    step_days: int = 1,
    datetime_handler: Callable[
        [datetime.datetime], datetime.date
    ] = datetime.datetime.date,
) -> Generator[datetime.date, None, None]:
    """date generator from start to end.

    Args:
        start (datetime.date | datetime.datetime): start date
        end (datetime.date | datetime.datetime | None, optional): end date.
            Defaults to None.
        include_start (bool, optional): include start date. Defaults to True.
        include_end (bool, optional): include end date. Defaults to True.
        step_days (int, optional): step days. Defaults to 1
        datetime_handler (Callable[[datetime.datetime], datetime.date], optional):
            function to convert datetime.datetime to datetime.date.
            Defaults to datetime.datetime.date.

    Yields:
        Generator[datetime.date, None, None]: date generator

    Raises:
        ValueError: step_days is 0
        TypeError: If start or end is not a datetime.date or datetime.datetime.

    Notes:
        - the generator will stop when it reaches out of range, that is,
          when the date is greater than date.max or less than date.min.
    """
    # validate step_days
    if step_days == 0:
        raise ValueError("step_days must not be 0")

    # validate and convert start and end to date
    validate_date_type(start)
    if end is not None:
        validate_date_type(end)

    if isinstance(start, datetime.datetime):
        start = datetime_handler(start)
    if isinstance(end, datetime.datetime):
        end = datetime_handler(end)

    # set ascending and delta
    ASCENDING = step_days > 0
    DELTA = datetime.timedelta(days=step_days)

    # set start date and end date
    if not include_start:
        start += DELTA
    if ASCENDING and end is None:
        end = datetime.date.max
    elif not ASCENDING and end is None:
        end = datetime.date.min
    assert end is not None

    # set end date
    is_broken: Callable[[datetime.date], bool] = {
        (True, True): end.__lt__,
        (True, False): end.__le__,
        (False, True): end.__gt__,
        (False, False): end.__ge__,
    }[(ASCENDING, include_end)]

    # yield date
    try:
        while not is_broken(start):
            yield start
            start += DELTA
    except OverflowError:
        pass
