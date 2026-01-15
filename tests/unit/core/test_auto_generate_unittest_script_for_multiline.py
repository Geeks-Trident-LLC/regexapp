"""
Automated unittest script generation tests.

This module validates the functionality of `RegexBuilder` and
`DynamicTestScriptBuilder` by comparing their generated unittest scripts
against a known expected output. It uses helper functions to provide
normalized test data and ensures consistency across test runs.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_autogenerate_unittest_script.py
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
        I have words(var_v1).
        My friend has words(var_v2).
        I don't have words(var_v3).
    """
    return user_data


@normalize_string_output
def get_test_data():
    """
    Provide normalized sample test data for unittest script validation.
    """
    test_data = """
        First line
        I have computer.
        Other line
        My friend has game console.
        Another line ....
        I don't have digital camera.
        ...
        last line
    """
    return test_data


class TestAutoGenerateUnittestScriptForMultiline:
    """
    Unit tests for automated unittest script generation.

    This class validates that both `RegexBuilder` and
    `DynamicTestScriptBuilder` produce unittest scripts identical to a
    reference script stored in `tests/unit/data/core/unittest_script_for_multiline.txt`.

    Notes
    -----
    - Both tests assert strict equality between generated and reference
      scripts, guaranteeing stability of automated script generation.
    - Metadata such as author, email, and company are passed into the
      builders to simulate realistic usage scenarios.
    """
    user_data = get_user_data()
    test_data = get_test_data()
    verified_test_script_filename = 'unittest_script_for_multiline.txt'

    def test_generating_unittest_using_regex_builder(self):
        """
        Verify that `RegexBuilder.create_unittest()` produces a unittest script
        identical to the expected reference output when the `is_line` flag
        is enabled (whole text regex generation).
        """

        factory = RegexBuilder(
            user_data=self.user_data,
            test_data=self.test_data,
            is_line=False,   # Instructs RegexApp to generate a whole text regex pattern
        )
        generated_test_script = factory.create_unittest()
        expected_test_script = get_test_script(self.verified_test_script_filename)
        assert generated_test_script == expected_test_script

    def test_generating_unittest_using_dynamic_test_script_builder(self):
        """
        Verify that `DynamicTestScriptBuilder.create_unittest()` produces a unittest
        script identical to the expected reference output when the `is_line` flag
        is disenabled (whole text regex generation).
        """
        factory = DynamicTestScriptBuilder(
            test_info=[self.user_data, self.test_data],
            is_line=False,   # Instructs RegexApp to generate a whole text regex pattern
        )
        generated_test_script = factory.create_unittest()
        expected_test_script = get_test_script(self.verified_test_script_filename)
        assert generated_test_script == expected_test_script
