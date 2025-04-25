import datetime
from functools import wraps
from logging import Logger, getLogger
from typing import Callable

from .date_range_utils import date_range

_logger = getLogger(__name__)
IsHolidayFuncType = Callable[[datetime.datetime | datetime.date], bool]  # noqa: E501


def is_saturday_or_sunday(
    date: datetime.datetime | datetime.date,
) -> bool:
    """Check if the given date is a Saturday or Sunday."

    Args:
        date (datetime.datetime | datetime.date): Date to check.

    Returns:
        bool: True if the date is a Saturday or Sunday, False otherwise.
    """
    return date.weekday() in {5, 6}


def is_new_year_day(
    date: datetime.datetime | datetime.date,
) -> bool:
    """Check if the given date is New Year's Day.

    Args:
        date (datetime.datetime | datetime.date): Date to check.

    Returns:
        bool: True if the date is New Year's Day, False otherwise.
    """
    return date.month == 1 and date.day == 1


def is_the_first_three_days_of_new_year(
    date: datetime.datetime | datetime.date,
) -> bool:
    """Check if the given date is within the first three days of the new year.

    Args:
        date (datetime.datetime | datetime.date): Date to check.

    Returns:
        bool: True if the date is within the first three days of the new year, False otherwise.
    """  # noqa: E501
    return date.month == 1 and date.day <= 3


def is_the_end_of_year(
    date: datetime.datetime | datetime.date,
) -> bool:
    """Check if the given date is the end of the year.

    Args:
        date (datetime.datetime | datetime.date): Date to check.

    Returns:
        bool: True if the date is the end of the year, False otherwise.
    """  # noqa: E501
    return date.month == 12 and date.day == 31


def is_between_1231_0103(
    date: datetime.datetime | datetime.date,
) -> bool:
    """Check if the given date is between December 31 and January 3.

    Args:
        date (datetime.datetime | datetime.date): Date to check.

    Returns:
        bool: True if the date is between December 31 and January 3, False otherwise.
    """
    return is_the_end_of_year(date) or is_the_first_three_days_of_new_year(date)


class HolidayDiscriminator:
    """Class to check if a date is a holiday.

    This class allows you to add custom holiday functions and check if a date is a holiday based on those functions.
    It also provides a way to remove holiday functions and get the names of the registered holiday functions.

    Args:
        *funcs (IsHolidayFuncType): Holiday functions to add.
        **kwargs (IsHolidayFuncType): Holiday functions to add.

    Properties:
        names (list[str]): List of names of the registered holiday functions.
        is_holiday_funcs (dict[str, IsHolidayFuncType]): Dictionary of the registered holiday functions.

    Methods:
        __call__(date: datetime.datetime | datetime.date) -> bool: Check if the given date is a holiday.
        add_is_holiday_funcs(*is_holiday_funcs_args: IsHolidayFuncType, **is_holiday_funcs_kwargs: IsHolidayFuncType) -> None: Add custom holiday functions.
        remove_is_holiday_funcs(*names: str) -> None: Remove holiday functions by their names.
    """  # noqa: E501

    def __init__(
        self,
        *funcs: IsHolidayFuncType,
        **kwargs: IsHolidayFuncType,
    ) -> None:
        self._is_holiday_funcs = {func.__name__: func for func in funcs}
        self._is_holiday_funcs.update(kwargs)

    def __call__(self, date: datetime.datetime | datetime.date) -> bool:
        """Check if the given date is a holiday.

        Args:
            date (datetime.datetime | datetime.date): Date to check.

        Returns:
            bool: True if the date is a holiday, False otherwise.
        """
        return any(func(date) for func in self._is_holiday_funcs.values())

    @property
    def names(self) -> list[str]:
        """Get the names of the registered holiday functions.

        Returns:
            list[str]: List of names of the registered holiday functions.
        """
        return list(self._is_holiday_funcs.keys())

    @property
    def is_holiday_funcs(self) -> dict[str, IsHolidayFuncType]:
        """Get the registered holiday functions.

        Returns:
            dict[str, IsHolidayFuncType]: Dictionary of the registered holiday functions.

        Notes:
            The returned dictionary is a shallow copy of the original dictionary.
            Modifications to the returned dictionary will not affect the original dictionary.
        """  # noqa: E501
        return self._is_holiday_funcs.copy()

    def add_is_holiday_funcs(
        self,
        *is_holiday_funcs_args: IsHolidayFuncType,
        allow_overwrite: bool = False,
        **is_holiday_funcs_kwargs: IsHolidayFuncType,
    ) -> None:
        """Add custom holiday functions.

        Args:
            *is_holiday_funcs_args (IsHolidayFuncType): Holiday functions to add.
            allow_overwrite (bool, optional): Allow overwriting existing holiday functions. Defaults to False.
            **is_holiday_funcs_kwargs (IsHolidayFuncType): Holiday functions to add.

        Raises:
            ValueError: If a function with the same name already exists and allow_overwrite is False.
            AttributeError: If the function does not have a __name__ attribute.

        Notes:
            - This method performs an all-or-nothing update: if there is an error, no functions will be added.
        """  # noqa: E501
        # preprocess
        dic: dict[str, IsHolidayFuncType] = {}
        for func in is_holiday_funcs_args:
            try:
                dic[func.__name__] = func
            except AttributeError as e:
                # TODO: more appropriate error handling
                raise e
        dic.update(is_holiday_funcs_kwargs)
        # check duplicates
        for name in dic.keys():
            if not allow_overwrite and name in self._is_holiday_funcs:
                raise ValueError(
                    f"Function with name '{name}' already exists. "
                    "Set allow_overwrite=True to overwrite."
                )
        # add the new functions
        for name, is_holiday_func in dic.items():
            # TODO: more strict type checking
            self._is_holiday_funcs[name] = is_holiday_func

    def remove_is_holiday_funcs(
        self,
        *names: str,
    ) -> None:
        """Remove holiday functions by their names.

        Raises:
            KeyError: If a function with the given name does not exist.

        Notes:
            - This method performs an all-or-nothing update: if there is an error, no functions will be removed.
        """  # noqa: E501
        # check if names are in the dictionary
        for name in names:
            if name not in self._is_holiday_funcs:
                raise KeyError(f"Function with name '{name}' does not exist.")
        # remove the functions
        for name in names:
            self._is_holiday_funcs.pop(name)


def compile_is_holiday(
    is_holiday: IsHolidayFuncType,
    start: datetime.datetime | datetime.date = datetime.date.min,
    end: datetime.datetime | datetime.date = datetime.date.max,
    logger: Logger = _logger,
) -> IsHolidayFuncType:
    """Compile a function to check if a date is a holiday.

    Args:
        is_holiday (IsHolidayFuncType): Function to compile.
        start (datetime.datetime | datetime.date, optional): Start date for
            compilation. Defaults to datetime.date.min.
        end (datetime.datetime | datetime.date, optional): End date for
            compilation. Defaults to datetime.date.max.
        logger (Logger, optional): Logger. Defaults to getLogger(__name__).

    Returns:
        IsHolidayFuncType: Compiled function.

    Note:
        - start and end dates are inclusive.
    """  # noqa: E501
    # Preprocess start and end dates
    if isinstance(start, datetime.datetime):
        start = start.date()
    if isinstance(end, datetime.datetime):
        end = end.date()

    # validate start and end dates
    if start > end:
        raise ValueError(
            "Start date must be before end date: "
            f"start = {start}, end = {end}"
        )

    # initialize the date range
    holidays: set[datetime.date] = {
        d
        for d in date_range(start, end)
        if is_holiday(d)
    }

    @wraps(is_holiday)
    def is_holiday_(d: datetime.datetime | datetime.date) -> bool:
        # Preprocess date
        if isinstance(d, datetime.datetime):
            d = d.date()
        # validate date
        if d < start or d > end:
            logger.warning(
                f"Date({d}) is out of the compilation range from {start} to {end}.",
            )
            return is_holiday(d)
        # Check if the date is in the set of holidays
        return d in holidays

    return is_holiday_
