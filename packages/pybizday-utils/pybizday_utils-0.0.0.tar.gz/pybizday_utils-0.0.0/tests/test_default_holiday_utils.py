from datetime import date

import pytest

from pybizday_utils.default_holiday_utils import (
    _GlobalDefaultHolidayDiscriminator,
    add_global_is_holiday_funcs,
    get_global_holiday_funcs,
    get_global_holiday_funcs_names,
    remove_global_is_holiday_funcs,
    with_is_holiday_funcs,
)
from pybizday_utils.holiday_utils import is_saturday_or_sunday


# mock functions for testing
def func1(d: date) -> bool:
    return d.day == 1


def func2(d: date) -> bool:
    return d.day == 2


def func3_(d: date) -> bool:
    return d.day == 3


def func_new(d: date) -> bool:
    return d.day == 4


def func_new2_(d: date) -> bool:
    return d.day == 5


@pytest.mark.positive
def test_global_default_holiday_discriminator_singleton() -> None:
    # Test that the singleton instance is the same across multiple calls
    instance1 = _GlobalDefaultHolidayDiscriminator.get_instance()
    instance2 = _GlobalDefaultHolidayDiscriminator.get_instance()
    assert instance1 is instance2, "Singleton instances are not the same"


@pytest.mark.positive
def test_get_global_holiday_funcs() -> None:
    # Test that the global holiday functions are empty by default
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    assert get_global_holiday_funcs() == {}, "Global holiday functions should be empty"  # noqa: E501

    default._is_holiday_funcs["test_func"] = lambda date: date.day == 1
    assert get_global_holiday_funcs() == {
        "test_func": default._is_holiday_funcs["test_func"],
    }

    default._is_holiday_funcs["test_func2"] = lambda date: date.day == 2
    assert get_global_holiday_funcs() == {
        "test_func": default._is_holiday_funcs["test_func"],
        "test_func2": default._is_holiday_funcs["test_func2"],
    }


@pytest.mark.positive
def test_get_global_holiday_funcs_names() -> None:
    # Test that the global holiday functions names are empty by default
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    assert get_global_holiday_funcs_names() == [], (
        "Global holiday functions names should be empty"
    )

    default._is_holiday_funcs["test_func"] = lambda date: date.day == 1
    assert get_global_holiday_funcs_names() == ["test_func"]

    default._is_holiday_funcs["test_func2"] = lambda date: date.day == 2
    assert get_global_holiday_funcs_names() == ["test_func", "test_func2"]


@pytest.mark.positive
def test_add_global_is_holiday_funcs() -> None:
    # execute
    add_global_is_holiday_funcs(func1, func2, func3=func3_)

    # check
    # NOTE: Assume that get_global_holiday_funcs works as expected.
    #       See test_get_global_holiday_funcs for the test.
    assert get_global_holiday_funcs()["func1"] == func1
    assert get_global_holiday_funcs()["func2"] == func2
    assert get_global_holiday_funcs()["func3"] == func3_


@pytest.mark.positive
def test_add_global_is_holiday_funcs_with_allow_overwrite() -> None:
    # preparation
    add_global_is_holiday_funcs(func1, func2, func3=func3_)

    # execute
    add_global_is_holiday_funcs(func1=func_new, allow_overwrite=True)

    # check
    # NOTE: Assume that get_global_holiday_funcs works as expected.
    #       See test_get_global_holiday_funcs for the test.
    assert get_global_holiday_funcs()["func1"] is func_new


@pytest.mark.negative
def test_add_global_is_holiday_funcs_should_prohibit_overwrite_in_default() -> None:  # noqa: E501
    # execute
    add_global_is_holiday_funcs(func1, func2, func3=func3_)

    # check
    with pytest.raises(ValueError):
        add_global_is_holiday_funcs(func1)
    with pytest.raises(ValueError):
        add_global_is_holiday_funcs(func2)
    with pytest.raises(ValueError):
        add_global_is_holiday_funcs(func3=func3_)


@pytest.mark.positive
def test_remove_global_is_holiday_funcs() -> None:
    # preparation
    add_global_is_holiday_funcs(func1, func2, func3=func3_)

    # execute
    remove_global_is_holiday_funcs("func1", "func3")

    # check
    # NOTE: Assume that get_global_holiday_funcs works as expected.
    #       See test_get_global_holiday_funcs for the test.
    assert "func1" not in get_global_holiday_funcs()
    assert "func3" not in get_global_holiday_funcs()
    assert "func2" in get_global_holiday_funcs()
    assert get_global_holiday_funcs()["func2"] is func2


@pytest.mark.negative
def test_remove_global_is_holiday_funcs_with_non_existing_name() -> None:
    # Test that removing a non-existing function name does not raise an error
    with pytest.raises(KeyError):
        remove_global_is_holiday_funcs("non_existing_func")


@pytest.mark.positive
def test_with_is_holiday_funcs_in_default() -> None:
    # preparation
    add_global_is_holiday_funcs(func1, func2, func3=func3_)
    assert get_global_holiday_funcs()["func1"] is func1
    assert get_global_holiday_funcs()["func2"] is func2
    assert get_global_holiday_funcs()["func3"] is func3_
    assert set(get_global_holiday_funcs_names()) == {"func1", "func2", "func3"}

    # execute and check
    with with_is_holiday_funcs(func_new):
        assert get_global_holiday_funcs()["func1"] is func1
        assert get_global_holiday_funcs()["func2"] is func2
        assert get_global_holiday_funcs()["func3"] is func3_
        assert get_global_holiday_funcs()["func_new"] is func_new
        assert set(get_global_holiday_funcs_names()) == {
            "func1",
            "func2",
            "func3",
            "func_new",
        }  # noqa: E501

    # check after exiting the context manager
    assert get_global_holiday_funcs()["func1"] is func1
    assert get_global_holiday_funcs()["func2"] is func2
    assert get_global_holiday_funcs()["func3"] is func3_
    assert "func_new" not in get_global_holiday_funcs()
    assert set(get_global_holiday_funcs_names()) == {"func1", "func2", "func3"}


@pytest.mark.positive
def test_with_is_holiday_funcs_with_allow_overwrite() -> None:
    # preparation
    add_global_is_holiday_funcs(func1, func2, func3=func3_)
    assert get_global_holiday_funcs()["func1"] is func1
    assert get_global_holiday_funcs()["func2"] is func2
    assert get_global_holiday_funcs()["func3"] is func3_
    assert set(get_global_holiday_funcs_names()) == {"func1", "func2", "func3"}  # noqa: E501

    # execute and check
    with with_is_holiday_funcs(func1=func_new, allow_overwrite=True):
        # check whether func1 is replaced by func_new
        assert get_global_holiday_funcs()["func1"] is func_new
        assert get_global_holiday_funcs()["func2"] is func2
        assert get_global_holiday_funcs()["func3"] is func3_
        assert set(get_global_holiday_funcs_names()) == {"func1", "func2", "func3"}  # noqa: E501

    # check after exiting the context manager
    # check whether func1 is restored to its original value
    assert get_global_holiday_funcs()["func1"] is func1
    assert get_global_holiday_funcs()["func2"] is func2
    assert get_global_holiday_funcs()["func3"] is func3_
    assert set(get_global_holiday_funcs_names()) == {"func1", "func2", "func3"}  # noqa: E501


@pytest.mark.positive
def test_with_is_holiday_funcs_with_all_replace() -> None:
    # preparation
    add_global_is_holiday_funcs(func1, func2, func3=func3_)
    assert get_global_holiday_funcs()["func1"] is func1
    assert get_global_holiday_funcs()["func2"] is func2
    assert get_global_holiday_funcs()["func3"] is func3_
    assert set(get_global_holiday_funcs_names()) == {"func1", "func2", "func3"}  # noqa: E501

    # execute and check
    with with_is_holiday_funcs(func_new, func_new2=func_new2_, all_replace=True):  # noqa: E501
        assert get_global_holiday_funcs()["func_new"] is func_new
        assert get_global_holiday_funcs()["func_new2"] is func_new2_
        assert "func1" not in get_global_holiday_funcs()
        assert "func2" not in get_global_holiday_funcs()
        assert "func3" not in get_global_holiday_funcs()
        assert set(get_global_holiday_funcs_names()) == {"func_new", "func_new2"}  # noqa: E501

    # check after exiting the context manager
    assert get_global_holiday_funcs()["func1"] is func1
    assert get_global_holiday_funcs()["func2"] is func2
    assert get_global_holiday_funcs()["func3"] is func3_
    assert "func_new" not in get_global_holiday_funcs()
    assert "func_new2" not in get_global_holiday_funcs()
    assert set(get_global_holiday_funcs_names()) == {"func1", "func2", "func3"}  # noqa: E501


@pytest.mark.positive
@pytest.mark.use_global_default_holiday_discriminator
def test_default_holiday_discriminator_status() -> None:
    # pereparation
    default = _GlobalDefaultHolidayDiscriminator.get_instance()
    name = is_saturday_or_sunday.__name__
    expected = is_saturday_or_sunday
    # check
    assert default.is_holiday_funcs[name] is expected
    assert get_global_holiday_funcs_names() == [name]
    assert get_global_holiday_funcs()[name] is expected
