"""
Automated python snippet test script generation tests.

This module validates the functionality of `RegexBuilder` and
`DynamicTestScriptBuilder` by comparing their generated python snippet scripts
against a known expected output. It uses helper functions to provide
normalized test data and ensures consistency across test runs.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_auto_generate_python_script_for_line_patterns.py
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
        words(var_v1, head)   words(var_v2, tail)
        words(var_v3, head)   number(var_v4, tail)
    """
    return user_data


@normalize_string_output
def get_test_data():
    """
    Provide normalized sample test data for snippet script validation.
    """
    test_data = """
        value1     9.99
        12.3       value 99
        value.10   value 11
        value20    value 21
        value99    N/A
    """
    return test_data


class TestAutoGeneratePythonTestScriptForLinePatterns:
    """
    Unit tests for automated python snippet test script generation.

    This class validates that both `RegexBuilder` and
    `DynamicTestScriptBuilder` produce python snippet scripts identical to a
    reference script stored in `tests/unit/data/core/snippet_script_for_line_patterns.txt`.

    Notes
    -----
    - Both tests assert strict equality between generated and reference
      scripts, guaranteeing stability of automated script generation.
    - Metadata such as author, email, and company are passed into the
      builders to simulate realistic usage scenarios.
    """
    user_data = get_user_data()
    test_data = get_test_data()
    verified_test_script_filename = 'snippet_script_for_line_patterns.txt'

    def test_generating_python_script_using_regex_builder(self):
        """
        Verify that `RegexBuilder.create_python_test()` produces a python test
        script identical to the expected reference output when the `is_line` flag
        is enabled (single-line regex generation).
        """

        factory = RegexBuilder(
            user_data=self.user_data,
            test_data=self.test_data,
            is_line=True,   # Instructs RegexApp to generate a single-line regex pattern
        )
        generated_test_script = factory.create_python_test()
        expected_test_script = get_test_script(self.verified_test_script_filename)
        assert generated_test_script == expected_test_script

    def test_generating_python_script_using_dynamic_test_script_builder(self):
        """
        Verify that `DynamicTestScriptBuilder.create_python_test()` produces
        a python test script identical to the expected reference output when
        the `is_line` flag is enabled (single-line regex generation).
        """
        factory = DynamicTestScriptBuilder(
            test_info=[self.user_data, self.test_data],
            is_line=True,   # Instructs RegexApp to generate a single-line regex pattern
        )
        generated_test_script = factory.create_python_test()
        expected_test_script = get_test_script(self.verified_test_script_filename)
        assert generated_test_script == expected_test_script
