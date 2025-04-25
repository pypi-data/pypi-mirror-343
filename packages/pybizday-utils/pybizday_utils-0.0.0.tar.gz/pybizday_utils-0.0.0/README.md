# `pybizday_utils`: Python Business Day Utilities :calendar:

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/pybizday_utils)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/pybizday_utils?sort=semver)
[![LICENSE](https://img.shields.io/github/license/hmasdev/pybizday_utils)](./LICENSE)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/pybizday_utils)
[![Scheduled Test](https://github.com/hmasdev/pybizday_utils/actions/workflows/on-scheduled.yaml/badge.svg)](https://github.com/hmasdev/pybizday_utils/actions/workflows/on-scheduled.yaml)
[![PyPI version](https://badge.fury.io/py/pybizday_utils.svg)](https://pypi.org/project/pybizday_utils/)

`pybizday_utils` is a Python library that provides utilities for calculating business days, including the ability to customize holidays and workdays.
It is designed to be simple and easy to use, making it a great choice for developers who need to work with business days in their applications.

## Installation

### Requirements

- Python 3.10 or later
- `pip`
- see [pyproject.toml](./pyproject.toml) for other dependencies

### Install `pybizday_utils` with pip

```bash
pip install -U pybizday_utils
```

```bash
pip install -U git+https://github.com/hmasdev/pybizday_utils.git
```

Note that the second command will install the latest version from the main branch, which may not be stable.

### Install `pybizday_utils` by building from source

See [How to Build](#how-to-build) section for more details.

## How to Use

`pybizday_utils` provides the following two main features:

1. **Calculate or count business days**:
   - get the n-th business day after a given date;
   - get the n-th business day before a given date;
   - get the iterator of business days between two dates;
   - count business days between two dates;
2. **Calculate business days in month**.
   - get the first business day of the month;
   - get the last business day of the month;
   - add years and months to a date considering business days. e.g. transform a business end of month to a business end of month.

In this section, some examples are provided to illustrate how to use the library.
If you want to know the details, see the docstrings of each function.

The following is an example of the first feature:

```python
from datetime import date
from pybizday_utils import (
    bizday_range,
    count_bizdays,
    get_n_next_bizday,
    get_n_prev_bizday,
    get_next_bizday,
    get_prev_bizday,
    is_bizday,
)

# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 3, 28))
print(next_bizday)  # Output: 2025-03-31

# Get the previous business day before a given date
prev_bizday = get_prev_bizday(date(2025, 3, 31))
print(prev_bizday)  # Output: 2025-03-28

# Get the n-th business day after a given date
n_next_bizday = get_n_next_bizday(date(2025, 3, 28), 2)
print(n_next_bizday)  # Output: 2025-04-01

# Get the n-th business day before a given date
n_prev_bizday = get_n_prev_bizday(date(2025, 3, 31), 2)
print(n_prev_bizday)  # Output: 2025-03-27
# Also works with negative numbers
n_prev_bizday_ = get_n_prev_bizday(date(2025, 3, 31), -2)
print(n_prev_bizday_)  # Output: 2025-03-27

# Get the iterator of business days between two dates
bizdays = bizday_range(date(2025, 3, 28), date(2025, 4, 4))
for bizday in bizdays:
    print(bizday)  # Output: 2025-03-28, 2025-03-31, 2025-04-01, 2025-04-02, 2025-04-03, 2025-04-04

# Count business days between two dates
count = count_bizdays(date(2025, 3, 28), date(2025, 4, 4))
print(count)  # Output: 6
```

On the other hand, the second feature is useful for calculating business days in a month. For example:

```python
from datetime import date
from pybizday_utils import (
    add_months,
    add_years,
    get_biz_start_of_month,
    get_biz_end_of_month,
)

# Get the first business day of the month
first_bizday = get_biz_start_of_month(date(2025, 3, 28))
print(first_bizday)  # Output: 2025-03-03

# Get the last business day of the month
last_bizday = get_biz_end_of_month(date(2024, 11, 15))
print(last_bizday)  # Output: 2024-11-29

# Add months to a date considering business days
add_months_bizday = add_months(date(2024, 10, 31), 1, bizeom2bizeom=True)
print(add_months_bizday)  # Output: 2024-11-29

# Add years to a date considering business days
add_years_bizday = add_years(date(2023, 11, 30), 1, bizeom2bizeom=True)
print(add_years_bizday)  # Output: 2024-11-29
```

**Note that only Saturday and Sunday are considered holidays in default**.
If you want to customize the holidays, see [Customize holidays](#customize-holidays) or [Customize the default holidays](#customize-the-default-holidays).

### Customize holidays

If you want to customize the holidays, pass `is_holiday` parameter to each function.
For example, you can use a lambda function to define your own holidays, assuming that 1/1 and 4/3 are holidays:

```python
from datetime import date
from pybizday_utils import (
    bizday_range,
    get_next_bizday,
    get_prev_bizday,
)

# Define your own holidays
def my_is_holiday(date):
   return date.month == 1 and date.day == 1 or date.month == 4 and date.day == 3


# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2), is_holiday=my_is_holiday)
print(next_bizday)  # Output: 2025-04-04

# Get the previous business day before a given date
prev_bizday = get_prev_bizday(date(2025, 4, 4), is_holiday=my_is_holiday)
print(prev_bizday)  # Output: 2025-04-02

# Get the iterator of business days between two dates
bizdays = bizday_range(date(2025, 4, 2), date(2025, 4, 6), is_holiday=my_is_holiday)
for bizday in bizdays:
    print(bizday)  # Output: 2025-04-02, 2025-04-04, 2025-04-05, 2025-04-06
```

**Note that the default `is_holiday function`, which checks if a date is Saturday or Sunday, is not used in this case.**

#### [Advanced] Compile Customized Holidays

If you find that `pybizday_utils` is slow, you can speed it up by compiling your holiday function.
The compile function provided in `pybizday_utils.holiday_utils` generates an optimized version of your holiday function.
This compiled function is faster because it uses a precomputed set of holiday dates.
Internally, it returns a function like `lambda d: d in HOLIDAY_SET`,
where `HOLIDAY_SET` is a set of dates for which your original holiday function returns True.

```python
from datetime import date
from pybizday_utils import get_next_bizday
from pybizday_utils.holiday_utils import compile_is_holiday


# Define your own holidays
def my_is_holiday(date):
   # ... Heavy calculation ...
   return date.month == 1 and date.day == 1 or date.month == 4 and date.day == 3


# Compile your holiday function
compiled_is_holiday = compile_is_holiday(my_is_holiday)

# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2), is_holiday=compiled_is_holiday)
print(next_bizday)  # Output: 2025-04-04
```

Furthermore, if you find that `compile_is_holiday` is slow, you can speed `compile_is_holiday` up by passing `start` and `end` parameters to `compile_is_holiday`.
`start` and `end` are the start and end dates of the range of dates you want to compile.

```python
from datetime import date
from pybizday_utils import get_next_bizday
from pybizday_utils.holiday_utils import compile_is_holiday


# Define your own holidays
def my_is_holiday(date):
   # ... Heavy calculation ...
   return date.month == 1 and date.day == 1 or date.month == 4 and date.day == 3

# Compile your holiday function with a range of dates
compiled_is_holiday = compile_is_holiday(my_is_holiday, start=date(2025, 1, 1), end=date(2025, 12, 31))

# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2), is_holiday=compiled_is_holiday)
print(next_bizday)  # Output: 2025-04-04
```

### Customize the default holidays

You can also customize the default holidays by using the `set_default_holidays` function.
This customization will affect all functions that use the default holidays.
For example, you can set the default holidays to be 1/1 and 4/3:

```python
from datetime import date
from pybizday_utils import (
    get_next_bizday,
    get_prev_bizday,
)
from pybizday_utils.default_holiday_utils import (
    add_global_is_holiday_funcs,
    remove_global_is_holiday_funcs,
)


def is_3rd_apr(date):
    return date.month == 4 and date.day == 3


# In default
# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2))
print(next_bizday)  # Output: 2025-04-03

# Add the global holidays
add_global_is_holiday_funcs(is_3rd_apr)

# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2))
print(next_bizday)  # Output: 2025-04-04

# Remove the global holidays
remove_global_is_holiday_funcs("is_3rd_apr")

# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2))
print(next_bizday)  # Output: 2025-04-03
```

If you want to customize the global default holidays temporarily, use `with_is_holiday_funcs` context manager.

For example:

```python
from datetime import date
from pybizday_utils import get_next_bizday
from pybizday_utils.default_holiday_utils import (
    with_is_holiday_funcs,
)


def is_3rd_apr(date):
    return date.month == 4 and date.day == 3


# In default
# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2))
print(next_bizday)  # Output: 2025-04-03

# Add the global holidays temporarily
with with_is_holiday_funcs(is_3rd_apr):
    # Get the next business day after a given date
    next_bizday = get_next_bizday(date(2025, 4, 2))
    print(next_bizday)  # Output: 2025-04-04

# Get the next business day after a given date
next_bizday = get_next_bizday(date(2025, 4, 2))
print(next_bizday)  # Output: 2025-04-03
```

## Contribution Guide

### Development Requirements

- Python 3.10 or later
- `uv`
- see [pyproject.toml](./pyproject.toml) for other dependencies

### How to Develop

1. Fork the repository: [https://github.com/hmasdev/pybizday_utils/fork](https://github.com/hmasdev/pybizday_utils/fork)
2. Clone the forked repository:

   ```bash
   git clone https://github.com/{your_username}/pybizday_utils
   cd pybizday_utils
   ```

3. Setup the development environment:

   ```bash
   uv sync --dev
   ```

4. Checkout your working branch:

   ```bash
   git switch -c {your_branch_name}
   # or
   # git checkout -b {your_branch_name}
   ```

5. Test and lint your changes and check type hints:

   ```bash
   uv run nox -s test
   uv run nox -s lint
   uv run nox -s mypy
   ```

   In above commands, each command is run with python 3.10, 3.11, 3.12, and 3.13.
   If you want to run with a specific version, use `--python` option. For example:

   ```bash
   uv run nox -s test --python 3.10
   uv run nox -s lint --python 3.11
   uv run nox -s mypy --python 3.12
   ```

   or

   ```bash
   uv run pytest
   uv run ruff check src tests
   uv run mypy src tests
   ```

6. Commit and push your changes:

   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin {your_branch_name}
   # git push -u origin {your_branch_name} # if you are pushing for the first time
   ```

7. [Create a pull request](https://github.com/hmasdev/pybizday_utils/compare) to the main repository.

### How to Build

1. Clone the forked repository:

   ```bash
   git clone https://github.com/hmasdev/pybizday_utils
   cd pybizday_utils
   ```

2. (optional) Checkout the branch you want to build:

   ```bash
   git switch {BRANCH_NAME}
   # or
   # git checkout {BRANCH_NAME_OR_COMMIT_HASH}
   ```

3. Setup the development environment:

   ```bash
   uv sync --dev
   ```

4. Build the package:

   ```bash
   uv build
   ```

5. See the built package in `dist` directory.

6. (optional) Upload the package to PyPI:

   ```bash
   uv run twine upload dist/*
   ```

   Note that `TWINE_USERNAME`, `TWINE_PASSWORD` and `TWINE_REPOSITORY_URL` environment variables must be set to valid values for [pybizday-utils](https://pypi.org/project/pybizday-utils/) project.

### How to Check the Code Performance

`check_performance.py` is provided to check the performance of the library.

This script measures the elapsed time of `get_n_next_bizday` functions with different values of `n` and `date` given in the command line arguments.

1. Clone the forked repository:

   ```bash
   git clone https://github.com/hmasdev/pybizday_utils
   cd pybizday_utils
   ```

2. (optional) Checkout the branch you want to build:

   ```bash
   git switch {BRANCH_NAME}
   # or
   # git checkout {BRANCH_NAME_OR_COMMIT_HASH}
   ```

3. Setup the development environment:

   ```bash
   uv sync --dev
   ```

4. Run the script:

   ```bash
   uv run check_performance.py --n 100000 --date 2025-01-01 --n-trials 100
   ```

   In this case, the command measures the elapsed time to calculate the 100,000-th business day after 2025-01-01, and repeat it 100 times.

## License

[MIT](./LICENSE)

## Author

- [hmasdev](https://github.com/hmasdev)
