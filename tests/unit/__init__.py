"""
Unit test utilities for the `tests.unit` package.

This module provides helper functions and decorators to streamline test setup
and ensure consistent formatting of test data:

Usage
-----
- Place reusable test scripts in `tests/unit/data/`.
- Call `get_test_script("example.txt")` to retrieve and prepare the script.
- Decorate helper functions with `@dedent_and_strip_data` to guarantee
  consistent string formatting across tests.
"""
import subprocess
from datetime import datetime
from pathlib import Path, PurePath
from textwrap import dedent
from functools import wraps

def get_test_script(filename):
    """
    Load and preprocess a test script file from the local `data/` directory.

    This function reads the contents of a specified test script file,
    replaces the placeholder string `_datetime_` with the current date
    formatted as `YYYY-MM-DD`, and returns the processed script text.

    Parameters
    ----------
    filename : str
        Name of the test script file located in `tests/unit/data/`.

    Returns
    -------
    str
        The full contents of the test script with `_datetime_` replaced
        by the current date string.

    Notes
    -----
    - Useful for injecting dynamic timestamps into test inputs.
    - Ensures test scripts remain reusable and consistent across runs.
    """

    dt_str = '{:%Y-%m-%d}'.format(datetime.now())

    base_dir = str(PurePath(Path(__file__).parent, 'data'))

    filename = str(PurePath(base_dir, filename))
    with open(filename) as stream:
        test_script = stream.read()
        test_script = test_script.replace('_datetime_', dt_str)
        return test_script



def normalize_string_output(func):
    """
    Decorator to standardize string output from a function.

    This wrapper ensures that any string returned by the decorated function
    is cleaned for consistent formatting. It applies `textwrap.dedent` to
    remove common leading whitespace and then strips leading/trailing
    whitespace characters.

    Parameters
    ----------
    func : Callable
        The function whose return value will be normalized.

    Returns
    -------
    Callable
        A wrapped function that returns a dedented and stripped string
        (or the original result if not a string).

    Notes
    -----
    - Useful in unit tests to guarantee predictable string formatting.
    - Helps avoid assertion mismatches caused by indentation or stray
      whitespace.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result = dedent(str(result)).strip()
        return result
    return wrapper


def get_package_info(pkg_name: str) -> str:
    """
    Retrieve package information from `pip freeze`.

    Parameters
    ----------
    pkg_name : str
        The name of the package to search for.

    Returns
    -------
    str
        The matching package specification (e.g., "pkg==1.2.3") if found.
        Otherwise, returns the full `pip freeze` output.
    """
    try:
        output = subprocess.check_output(
            ["pip", "freeze"], stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        return f"Error running pip freeze: {e.output}"

    # Find lines that start with the package name (case-insensitive match optional)
    matches = [line.strip() for line in output.splitlines() if line.startswith(pkg_name)]

    return matches[0] if matches else output
