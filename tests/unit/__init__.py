"""
Unit test utilities for the `tests.unit` package.

Run pytest in the project root to execute these tests:
    $ pytest
    $ pytest tests/unit
    or
    $ python -m pytest
    $ python -m pytest tests/unit
"""

from datetime import datetime
from pathlib import Path, PurePath

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
