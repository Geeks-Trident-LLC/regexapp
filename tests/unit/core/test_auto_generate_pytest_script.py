"""
Automated pytest script generation tests.

This module validates the functionality of `RegexBuilder` and
`DynamicTestScriptBuilder` by comparing their generated pytest scripts
against a known expected output. It uses helper functions to provide
normalized test data and ensures consistency across test runs.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/core/test_autogenerate_pytest_script.py
"""


from regexapp import RegexBuilder
from regexapp import DynamicTestScriptBuilder

from tests.unit import get_test_script         # import from tests/unit/__init__.py
from tests.unit import normalize_string_output # import from tests/unit/__init__.py


@normalize_string_output
def get_user_data():
    """
    Provide normalized sample user data for test script generation.
    """
    user_data = """
        phrase(var_subject) is digits(var_degree) degrees word(var_unit).
           IPv4 Address. . . . . . . . . . . : ipv4_address(var_ipv4_addr)(word(var_status))
    """
    return user_data


@normalize_string_output
def get_test_data():
    """
    Provide normalized sample test data for pytest script validation.
    """
    test_data = """
        today temperature is 75 degrees fahrenheit.
        the highest temperature ever recorded on Earth is 134 degrees fahrenheit.
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)
    """
    return test_data


class TestAutoGeneratePytestScript:
    """
    Unit tests for automated pytest script generation.

    This class validates that both `RegexBuilder` and
    `DynamicTestScriptBuilder` produce pytest scripts identical to a
    reference script stored in `tests/unit/data/pytest_script.txt`.

    Notes
    -----
    - Both tests assert strict equality between generated and reference
      scripts, guaranteeing stability of automated script generation.
    - Metadata such as author, email, and company are passed into the
      builders to simulate realistic usage scenarios.
    """
    user_data = get_user_data()
    test_data = get_test_data()
    verified_test_script_filename = 'pytest_script.txt'

    def test_generating_pytest_using_regex_builder(self):
        """
        Verify that `RegexBuilder.create_pytest()` produces a pytest script
        identical to the expected reference output when the `is_line` flag
        is enabled (single-line regex generation).
        """

        factory = RegexBuilder(
            user_data=self.user_data,
            test_data=self.test_data,
            is_line=True,   # Instructs RegexApp to generate a single-line regex pattern
        )
        generated_test_script = factory.create_pytest()
        expected_test_script = get_test_script(self.verified_test_script_filename)
        assert generated_test_script == expected_test_script

    def test_generating_pytest_using_dynamic_test_script_builder(self):
        """
        Verify that `DynamicTestScriptBuilder.create_pytest()` produces a pytest
        script identical to the expected reference output when the `is_line` flag
        is enabled (single-line regex generation).
        """
        factory = DynamicTestScriptBuilder(
            test_info=[self.user_data, self.test_data],
            is_line=True,   # Instructs RegexApp to generate a single-line regex pattern
        )
        generated_test_script = factory.create_pytest()
        expected_test_script = get_test_script(self.verified_test_script_filename)
        assert generated_test_script == expected_test_script
