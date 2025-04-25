from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from .holiday_utils import (
    HolidayDiscriminator,
    IsHolidayFuncType,
    is_saturday_or_sunday,
)


class _GlobalDefaultHolidayDiscriminator(HolidayDiscriminator):
    """Singleton class to manage the global default holiday functions.
    This class is a singleton that holds the default holiday functions.

    See Also:
        - HolidayDiscriminator: The base class for managing holiday functions.
    """

    _instance: _GlobalDefaultHolidayDiscriminator | None = None

    def __new__(cls, *args, **kwargs) -> _GlobalDefaultHolidayDiscriminator:  # type: ignore  # noqa: E501
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_instance(cls) -> _GlobalDefaultHolidayDiscriminator:
        """Get the singleton instance of the class.

        Returns:
            _GlobalDefaultHolidayDiscriminator: The singleton instance of the class.
        """  # noqa: E501
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_global_holiday_funcs_names() -> list[str]:
    """Get the names of the registered holiday functions.

    Returns:
        list[str]: List of names of the registered holiday functions in the global default holiday discriminator.
    """  # noqa: E501
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    return default.names


def get_global_holiday_funcs() -> dict[str, IsHolidayFuncType]:
    """Get the registered holiday functions.

    Returns:
        dict[str, IsHolidayFuncType]: Dictionary of the registered holiday functions in the global default holiday discriminator.

    Notes:
        The returned dictionary is a shallow copy of the original dictionary.
        Modifications to the returned dictionary will not affect the original dictionary.
    """  # noqa: E501
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    return default.is_holiday_funcs


@contextmanager
def with_is_holiday_funcs(
    *is_holiday_funcs_args: IsHolidayFuncType,
    allow_overwrite: bool = False,
    all_replace: bool = False,
    **is_holiday_funcs_kwargs: IsHolidayFuncType,
) -> Generator[HolidayDiscriminator, None, None]:
    """Context manager to add custom holiday functions.
    This context manager allows you to customize the holiday functions used in the global default holiday discriminator temporarily.

    Args:
        *is_holiday_funcs_args (IsHolidayFuncType): Custom holiday functions to add.
        allow_overwrite (bool, optional): Whether to allow overwriting existing holiday functions. Defaults to False.
        all_replace (bool, optional): Whether to remove all current holiday functions before adding new ones. Defaults to False.
        **is_holiday_funcs_kwargs (IsHolidayFuncType): Custom holiday functions to add.

    Yields:
        Generator[HolidayDiscriminator, None, None]: The global default holiday discriminator with the added holiday functions.

    Notes:
        - The context manager will restore the original state of the holiday functions after exiting the context.
        - If `all_replace` is set to True, all current holiday functions will be removed before adding new ones.
        - If `allow_overwrite` is set to True, existing holiday functions with the same name will be overwritten.
    """  # noqa: E501

    # Get the default holiday discriminator instance
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    # Cache the current holiday functions
    _cache = default.is_holiday_funcs

    # If all_replace is True, remove all current holiday functions
    if all_replace:
        default.remove_is_holiday_funcs(*default.names)

    # add the new holiday functions
    default.add_is_holiday_funcs(
        *is_holiday_funcs_args,
        allow_overwrite=allow_overwrite,
        **is_holiday_funcs_kwargs,
    )

    try:
        yield default
    finally:
        # remove all holiday functions
        default.remove_is_holiday_funcs(*default.names)
        # Restore the original state
        default.add_is_holiday_funcs(**_cache, allow_overwrite=True)


# initialize the default holiday functions
global_default_holiday_discriminator = _GlobalDefaultHolidayDiscriminator.get_instance()  # noqa: E501
global_default_holiday_discriminator.add_is_holiday_funcs(
    is_saturday_or_sunday,
    allow_overwrite=True,
)
add_global_is_holiday_funcs = global_default_holiday_discriminator.add_is_holiday_funcs  # noqa: E501
remove_global_is_holiday_funcs = (
    global_default_holiday_discriminator.remove_is_holiday_funcs
)
