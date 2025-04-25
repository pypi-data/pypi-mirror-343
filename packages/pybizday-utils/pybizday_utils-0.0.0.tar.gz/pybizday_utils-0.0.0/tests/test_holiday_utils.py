from datetime import date, datetime

import pytest

from pybizday_utils.holiday_utils import (
    HolidayDiscriminator,
    IsHolidayFuncType,
    compile_is_holiday,
    is_between_1231_0103,
    is_new_year_day,
    is_saturday_or_sunday,
    is_the_end_of_year,
    is_the_first_three_days_of_new_year,
)


@pytest.mark.positive
@pytest.mark.parametrize(
    "d, expected",
    [
        (date(2025, 3, 21), False),
        (date(2025, 3, 22), True),
        (date(2025, 3, 23), True),
        (date(2025, 3, 24), False),
        (datetime(2025, 3, 21), False),
        (datetime(2025, 3, 22), True),
        (datetime(2025, 3, 23), True),
        (datetime(2025, 3, 24), False),
    ],
)
def test_is_saturday_or_sunday(
    d: datetime | date,
    expected: bool,
) -> None:
    assert is_saturday_or_sunday(d) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d, expected",
    [
        (date(2025, 1, 1), True),
        (date(2025, 1, 2), False),
        (datetime(2024, 1, 1), True),
        (datetime(2024, 1, 2), False),
    ],
)
def test_is_new_year_day(
    d: datetime | date,
    expected: bool,
) -> None:
    assert is_new_year_day(d) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d, expected",
    [
        (date(2024, 12, 31), False),
        (date(2025, 1, 1), True),
        (date(2025, 1, 2), True),
        (date(2025, 1, 3), True),
        (date(2025, 1, 4), False),
        (datetime(2024, 12, 31), False),
        (datetime(2024, 1, 1), True),
        (datetime(2024, 1, 2), True),
        (datetime(2024, 1, 3), True),
        (datetime(2024, 1, 4), False),
    ],
)
def test_is_the_first_three_days_of_new_year(
    d: datetime | date,
    expected: bool,
) -> None:
    assert is_the_first_three_days_of_new_year(d) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d, expected",
    [
        (date(2024, 12, 30), False),
        (date(2024, 12, 31), True),
        (date(2025, 1, 1), False),
        (date(2025, 1, 2), False),
        (datetime(2024, 12, 30), False),
        (datetime(2024, 12, 31), True),
        (datetime(2025, 1, 1), False),
        (datetime(2025, 1, 2), False),
    ],
)
def test_is_the_end_of_year(
    d: datetime | date,
    expected: bool,
) -> None:
    assert is_the_end_of_year(d) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "d, expected",
    [
        (date(2024, 12, 30), False),
        (date(2024, 12, 31), True),
        (date(2025, 1, 1), True),
        (date(2025, 1, 2), True),
        (date(2025, 1, 3), True),
        (date(2025, 1, 4), False),
        (datetime(2024, 12, 30), False),
        (datetime(2024, 12, 31), True),
        (datetime(2025, 1, 1), True),
        (datetime(2025, 1, 2), True),
        (datetime(2025, 1, 3), True),
        (datetime(2025, 1, 4), False),
    ],
)
def test_is_between_1231_0103(
    d: datetime | date,
    expected: bool,
) -> None:
    assert is_between_1231_0103(d) == expected


@pytest.mark.positive
def test_holiday_discriminator_with_arg() -> None:
    discriminator = HolidayDiscriminator(is_saturday_or_sunday)
    assert discriminator(date(2025, 3, 21)) is False
    assert discriminator(date(2025, 3, 22)) is True
    assert discriminator(date(2025, 3, 23)) is True
    assert discriminator(date(2025, 3, 24)) is False
    assert discriminator.names == [is_saturday_or_sunday.__name__]


@pytest.mark.positive
def test_holiday_discriminator_with_kwarg() -> None:
    discriminator = HolidayDiscriminator(is_sos=is_saturday_or_sunday)
    assert discriminator(date(2025, 3, 21)) is False
    assert discriminator(date(2025, 3, 22)) is True
    assert discriminator(date(2025, 3, 23)) is True
    assert discriminator(date(2025, 3, 24)) is False
    assert discriminator.names == ["is_sos"]


@pytest.mark.positive
def test_holiday_discriminator_with_args_kwargs() -> None:
    discriminator = HolidayDiscriminator(
        is_saturday_or_sunday,
        is_new_year_day,
        is_eoy=is_the_end_of_year,
        is_20250325=lambda d: d == date(2025, 3, 25),
    )
    assert discriminator(date(2025, 3, 21)) is False
    assert discriminator(date(2025, 3, 22)) is True
    assert discriminator(date(2025, 3, 23)) is True
    assert discriminator(date(2025, 3, 24)) is False
    assert discriminator(date(2025, 1, 1)) is True
    assert discriminator(date(2025, 1, 2)) is False
    assert discriminator(date(2024, 12, 30)) is False
    assert discriminator(date(2024, 12, 31)) is True
    assert discriminator(date(2025, 3, 25)) is True
    assert discriminator(date(2025, 3, 26)) is False
    assert discriminator.names == [
        is_saturday_or_sunday.__name__,
        is_new_year_day.__name__,
        "is_eoy",
        "is_20250325",
    ]


@pytest.mark.positive
def test_holiday_discriminator_kwargs_priority() -> None:
    def dummy(date: date) -> bool:
        raise NotImplementedError()

    # use dummy function when dummy is not overwritten by kwargs
    discriminator = HolidayDiscriminator(dummy)
    with pytest.raises(NotImplementedError):
        discriminator(date(2025, 1, 1))
    assert discriminator.names == ["dummy"]

    # use is_new_year_day when dummy is overwritten by kwargs
    discriminator = HolidayDiscriminator(dummy, dummy=is_new_year_day)  # noqa: E501
    assert discriminator(date(2025, 1, 1)) is True
    assert discriminator(date(2025, 1, 2)) is False
    assert discriminator.names == ["dummy"]


@pytest.mark.positive
def test_holiday_discriminator_properties() -> None:
    discriminator = HolidayDiscriminator(is_new_year_day)
    assert discriminator.names == list(discriminator._is_holiday_funcs.keys())
    assert discriminator.is_holiday_funcs == discriminator._is_holiday_funcs

    discriminator._is_holiday_funcs["func"] = is_saturday_or_sunday
    assert discriminator.names == list(discriminator._is_holiday_funcs.keys())
    assert discriminator.is_holiday_funcs == discriminator._is_holiday_funcs

    discriminator._is_holiday_funcs["func"] = is_between_1231_0103
    assert discriminator.names == list(discriminator._is_holiday_funcs.keys())
    assert discriminator.is_holiday_funcs == discriminator._is_holiday_funcs

    discriminator._is_holiday_funcs["func2"] = is_the_end_of_year
    assert discriminator.names == list(discriminator._is_holiday_funcs.keys())
    assert discriminator.is_holiday_funcs == discriminator._is_holiday_funcs

    discriminator._is_holiday_funcs.pop("func")
    assert discriminator.names == list(discriminator._is_holiday_funcs.keys())
    assert discriminator.is_holiday_funcs == discriminator._is_holiday_funcs


@pytest.mark.positive
def test_holiday_discriminator_add_is_holiday_funcs_as_args() -> None:
    discriminator = HolidayDiscriminator()
    assert discriminator(date(2025, 1, 1)) is False
    assert discriminator.names == []
    cache = discriminator._is_holiday_funcs.copy()

    discriminator.add_is_holiday_funcs(is_new_year_day)
    assert discriminator(date(2025, 1, 1)) is True
    assert discriminator.names == [is_new_year_day.__name__]

    # Just in case
    assert discriminator._is_holiday_funcs != cache


@pytest.mark.positive
def test_holiday_discriminator_add_is_holiday_funcs_as_kwargs() -> None:
    discriminator = HolidayDiscriminator()
    assert discriminator(date(2025, 1, 1)) is False
    assert discriminator.names == []
    cache = discriminator._is_holiday_funcs.copy()

    discriminator.add_is_holiday_funcs(inyd=is_new_year_day)
    assert discriminator(date(2025, 1, 1)) is True
    assert discriminator.names == ["inyd"]

    # Just in case
    assert discriminator._is_holiday_funcs != cache


@pytest.mark.positive
def test_holiday_discriminator_add_is_holiday_funcs_with_allow_overwrite() -> None:
    discriminator = HolidayDiscriminator(func=is_new_year_day)
    assert discriminator(date(2025, 1, 1)) is True
    assert discriminator.names == ["func"]
    cache = discriminator._is_holiday_funcs.copy()

    discriminator.add_is_holiday_funcs(func=is_saturday_or_sunday, allow_overwrite=True)  # noqa
    assert discriminator(date(2025, 1, 1)) is False
    assert discriminator.names == ["func"]

    # Just in case
    assert discriminator._is_holiday_funcs != cache


@pytest.mark.negative
def test_holiday_discriminator_add_is_holiday_funcs_should_prohibit_overwrite_in_default() -> (  # noqa: E501
    None
):
    discriminator = HolidayDiscriminator(func=is_new_year_day)
    assert discriminator(date(2025, 1, 1)) is True
    assert discriminator.names == ["func"]
    cache = discriminator._is_holiday_funcs.copy()

    with pytest.raises(ValueError):
        discriminator.add_is_holiday_funcs(
            is_the_end_of_year,
            funb=is_the_end_of_year,
            func=is_saturday_or_sunday,
            fund=is_new_year_day,
        )
    assert discriminator(date(2025, 1, 1)) is True

    # NOTE: Ensure all or nothing is updated. # noqa: E501
    assert discriminator.names == ["func"]

    # Just in case
    # NOTE: Ensure all or nothing is updated.
    assert discriminator._is_holiday_funcs == cache


@pytest.mark.negative
def test_holiday_discriminator_add_is_holiday_funcs_as_args_without_name_attr() -> None:  # noqa: E501
    class CallableCls:
        def __call__(self, d: date) -> bool:
            return d == d

    callable_instance = CallableCls()
    assert not hasattr(callable_instance, "__name__")

    discriminator = HolidayDiscriminator()
    cache = discriminator._is_holiday_funcs.copy()

    with pytest.raises(AttributeError):
        discriminator.add_is_holiday_funcs(
            is_new_year_day,
            callable_instance,
            is_saturday_or_sunday,
            func=is_the_end_of_year,
        )

    # NOTE: Ensure all or nothing is updated.
    assert discriminator.names == []

    # Just in case
    # NOTE: Ensure all or nothing is updated.
    assert discriminator._is_holiday_funcs == cache


@pytest.mark.positive
def test_holiday_discriminator_remove() -> None:
    discriminator = HolidayDiscriminator(is_new_year_day)
    assert discriminator(date(2025, 1, 1)) is True
    assert discriminator.names == [is_new_year_day.__name__]

    discriminator.remove_is_holiday_funcs(is_new_year_day.__name__)
    assert discriminator(date(2025, 1, 1)) is False
    assert discriminator.names == []


@pytest.mark.negative
def test_holiday_discriminator_remove_not_exist() -> None:
    discriminator = HolidayDiscriminator(is_new_year_day)
    assert discriminator.names == [is_new_year_day.__name__]
    with pytest.raises(KeyError):
        discriminator.remove_is_holiday_funcs(
            is_new_year_day.__name__,
            is_saturday_or_sunday.__name__,
        )

    # NOTE: Ensure all or nothing is updated.
    assert discriminator.names == [is_new_year_day.__name__]


@pytest.mark.positive
@pytest.mark.heavy
@pytest.mark.parametrize(
    "is_holiday",
    [
        is_new_year_day,
        is_saturday_or_sunday,
        is_the_end_of_year,
        is_the_first_three_days_of_new_year,
    ],
)
def test_compile(
    is_holiday: IsHolidayFuncType,
) -> None:

    # check whether compile works
    compiled_func = compile_is_holiday(is_holiday)

    # check whether compiled function works as expected
    for d in [
        date(2024, 12, 30),
        date(2024, 12, 31),
        date(2025, 1, 1),
        date(2025, 1, 2),
        datetime(2025, 1, 3),
        datetime(2025, 1, 4),
        datetime(2025, 1, 5),
        datetime(2025, 1, 6),
    ]:
        assert compiled_func(d) == is_holiday(d)


@pytest.mark.positive
@pytest.mark.heavy
@pytest.mark.parametrize(
    "is_holiday, start, end",
    [
        (
            is_new_year_day,
            date(2019, 1, 1),
            date(2030, 12, 31),
        ),
        (
            is_saturday_or_sunday,
            date(2020, 1, 1),
            date(2030, 12, 31),
        ),
        (
            is_the_end_of_year,
            datetime(2020, 1, 1),
            datetime(2031, 12, 31),
        ),
        (
            is_the_first_three_days_of_new_year,
            datetime(2020, 1, 1),
            datetime(2031, 12, 31),
        ),
    ],
)
def test_compile_with_start_and_end(
    is_holiday: IsHolidayFuncType,
    start: date,
    end: date,
) -> None:

    # check whether compile works
    compiled_func = compile_is_holiday(is_holiday, start, end)

    # check whether compiled function works as expected
    for d in [
        date(2024, 12, 30),
        date(2024, 12, 31),
        date(2025, 1, 1),
        date(2025, 1, 2),
        datetime(2025, 1, 3),
        datetime(2025, 1, 4),
        datetime(2025, 1, 5),
        datetime(2025, 1, 6),
    ]:
        assert compiled_func(d) == is_holiday(d)


@pytest.mark.positive
def test_compiled_func_for_out_of_compilation_range(
    caplog: pytest.LogCaptureFixture,
) -> None:

    start = date(2020, 1, 1)
    end = date(2030, 12, 31)
    d = date(2019, 1, 1)
    compiled_func = compile_is_holiday(is_new_year_day, start=start, end=end)

    # execute the compiled function with a date out of the compilation range
    with caplog.at_level("WARNING"):
        compiled_func(date(2019, 1, 1))

    expected = f"Date({d}) is out of the compilation range from {start} to {end}."  # noqa: E501
    assert expected in caplog.text


@pytest.mark.negative
def test_compile_with_start_is_greater_than_end() -> None:
    with pytest.raises(ValueError):
        compile_is_holiday(
            is_new_year_day,
            start=date(2030, 1, 1),
            end=date(2020, 12, 31),
        )
