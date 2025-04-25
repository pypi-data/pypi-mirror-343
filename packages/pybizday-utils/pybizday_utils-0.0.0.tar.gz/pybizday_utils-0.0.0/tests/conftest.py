from typing import Generator

import pytest


@pytest.fixture(autouse=True)
def deactivate_global_default_holiday_discriminator(
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    if request.node.get_closest_marker("use_global_default_holiday_discriminator"):  # noqa: E501
        # Skip this fixture if the test is marked with "use_default_holiday_discriminator" # noqa: E501
        yield
    else:
        from pybizday_utils.default_holiday_utils import (
            global_default_holiday_discriminator,
        )  # noqa: I001

        # FIXME: safer way to deactivate the default holiday discriminator.
        #        implement the following codes to avoid use the functions which are tested in test/default_holiday_utils.py  # noqa: E501
        cache = global_default_holiday_discriminator._is_holiday_funcs.copy()
        global_default_holiday_discriminator._is_holiday_funcs = {}
        try:
            yield
        finally:
            global_default_holiday_discriminator._is_holiday_funcs = cache
