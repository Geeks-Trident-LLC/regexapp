"""
Unit tests for regexapp pattern creation and reference management.

This module validates the functionality of `RegexBuilder` and the
reference management utilities (`add_reference`, `remove_reference`)
provided by regexapp. It ensures that regex patterns are correctly
built, tested against sample data, and produce expected reports.

Helpers
-------
get_user_data() -> str
    Returns normalized sample user data with placeholder variables
    for subjects, degrees, units, and IPv4 addresses.
get_test_data() -> str
    Returns normalized sample test data with concrete values for
    temperatures and IPv4 addresses.
get_test_report() -> str
    Returns a normalized sample test report showing expected matches
    for subject, degree, unit, and IPv4 address patterns.
get_other_user_data() -> str
    Returns normalized sample user data with placeholders for file
    attributes such as type, permission, owner, group, size, date,
    time, and filename.
get_other_test_data() -> str
    Returns normalized sample test data with concrete file listings.
get_other_test_report() -> str
    Returns a normalized sample test report showing expected matches
    for file attributes.

Tests
-----
TestRegexBuilder.test_regex_builder_creation
    Verifies that `RegexBuilder` builds and tests regex patterns
    correctly, producing a report identical to the expected output.
test_add_reference
    Confirms that custom references can be added and used in regex
    pattern creation, producing the expected report.
test_remove_reference
    Ensures that a previously added reference can be removed without
    error.
test_add_reference_exception
    Validates that attempting to remove or re-remove references raises
    `PatternReferenceError` as expected.

Notes
-----
- All helper functions are decorated with `normalize_string_output`
  to guarantee consistent formatting of returned strings.
- These tests assert strict equality between generated and expected
  reports, ensuring regex patterns remain stable and predictable.
"""


import pytest
from regexapp import RegexBuilder
from regexapp import add_reference
from regexapp import remove_reference
from regexapp.exceptions import PatternReferenceError

from tests.unit import normalize_string_output # import from tests/unit/__init__.py


@normalize_string_output
def get_user_data():
    """
    Provide normalized sample user data for regexapp pattern creation.
    """
    user_data = """
        phrase(var_subject) is digits(var_degree) degrees word(var_unit).
           IPv4 Address. . . . . . . . . . . : ipv4_address(var_ipv4_addr)(word(var_status))
    """
    return user_data


@normalize_string_output
def get_test_data():
    """
    Provide normalized sample test data for regexapp pattern creation.
    """
    test_data = """
        today temperature is 75 degrees fahrenheit.
        the highest temperature ever recorded on Earth is 134 degrees fahrenheit.
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)
    """
    return test_data


@normalize_string_output
def get_test_report():
    """
    Provide normalized sample test report for regexapp pattern verification.
    """
    test_report = """
        Test Data:
        ---------
        today temperature is 75 degrees fahrenheit.
        the highest temperature ever recorded on Earth is 134 degrees fahrenheit.
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)

        Matched Result:
        --------------
        pattern: (?P<subject>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)+) is (?P<degree>\\d+) degrees (?P<unit>[a-zA-Z][a-zA-Z0-9]*)\\.
        matched: [{'subject': 'today temperature', 'degree': '75', 'unit': 'fahrenheit'}, {'subject': 'the highest temperature ever recorded on Earth', 'degree': '134', 'unit': 'fahrenheit'}]
        ----------
        pattern:  +IPv4 Address(\\. ){2,}: (?P<ipv4_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3})\\((?P<status>[a-zA-Z][a-zA-Z0-9]*)\\)
        matched: [{'ipv4_addr': '192.168.0.1', 'status': 'Preferred'}]
        ----------
    """
    return test_report


@normalize_string_output
def get_other_user_data():
    """
    Provide normalized sample user data for regexapp pattern creation.
    """
    user_data = """
        file_type(var_file_type)file_permission(var_file_permission) digits(var_hard_links) word(var_file_owner) word(var_file_group)  digits(var_file_size) month_day(var_date) hour_minute(var_time) mixed_words(var_filename)
    """
    return user_data


@normalize_string_output
def get_other_test_data():
    """
    Provide normalized sample test data for regexapp pattern creation.
    """
    test_data = """
        -rw-r--r-- 1 abc staff  133 Jun 10 20:33 README.md
        -rw-r--r-- 1 abc staff 1488 Jul 27 00:48 setup.py
        drwxr-xr-x 1 abc staff    0 Jul  7 15:33 tests/
    """
    return test_data


@normalize_string_output
def get_other_test_report():
    """
    Provide normalized sample test report for regexapp pattern verification.
    """
    test_report = """
        Test Data:
        ---------
        -rw-r--r-- 1 abc staff  133 Jun 10 20:33 README.md
        -rw-r--r-- 1 abc staff 1488 Jul 27 00:48 setup.py
        drwxr-xr-x 1 abc staff    0 Jul  7 15:33 tests/

        Matched Result:
        --------------
        pattern: (?P<file_type>\\S)(?P<file_permission>\\S+) (?P<hard_links>\\d+) (?P<file_owner>[a-zA-Z][a-zA-Z0-9]*) (?P<file_group>[a-zA-Z][a-zA-Z0-9]*) +(?P<file_size>\\d+) (?P<date>[a-zA-Z]{3} +\\d{1,2}) (?P<time>\\d+:\\d+) (?P<filename>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)*)
        matched: [{'file_type': '-', 'file_permission': 'rw-r--r--', 'hard_links': '1', 'file_owner': 'abc', 'file_group': 'staff', 'file_size': '133', 'date': 'Jun 10', 'time': '20:33', 'filename': 'README.md'}, {'file_type': '-', 'file_permission': 'rw-r--r--', 'hard_links': '1', 'file_owner': 'abc', 'file_group': 'staff', 'file_size': '1488', 'date': 'Jul 27', 'time': '00:48', 'filename': 'setup.py'}, {'file_type': 'd', 'file_permission': 'rwxr-xr-x', 'hard_links': '1', 'file_owner': 'abc', 'file_group': 'staff', 'file_size': '0', 'date': 'Jul  7', 'time': '15:33', 'filename': 'tests/'}]
        ----------
    """
    return test_report


class TestRegexBuilder:
    def test_regex_builder_creation(self):
        """
            Verifies that `RegexBuilder` builds and tests regex patterns
            correctly, producing a report identical to the expected output.
        """
        factory = RegexBuilder(
            user_data=get_user_data(),
            test_data=get_test_data(),
            is_line=True
        )
        factory.build()
        factory.test()

        assert factory.test_result is True
        expected_test_report = get_test_report()
        assert factory.test_report == expected_test_report


def test_add_reference():
    """
    Confirms that custom references can be added and used in regex
    pattern creation, producing the expected report.
    """
    add_reference(name='file_type', pattern=r'\S')
    add_reference(name='file_permission', pattern=r'\S+')
    add_reference(name='month_day', pattern=r'[a-zA-Z]{3} +\d{1,2}')
    add_reference(name='hour_minute', pattern=r'\d+:\d+')

    factory = RegexBuilder(
        user_data=get_other_user_data(),
        test_data=get_other_test_data(),
        is_line=True
    )
    factory.build()
    factory.test()
    assert factory.test_result is True
    expected_test_report = get_other_test_report()
    assert factory.test_report == expected_test_report


def test_remove_reference():
    """
    Ensures that a previously added reference can be removed without error.
    """
    add_reference(name='month_day', pattern=r'[a-zA-Z]{3} +\d{1,2}')
    remove_reference(name='month_day')


def test_add_reference_exception():
    """
    Validates that attempting to remove or re-remove references raises
    `PatternReferenceError` as expected.
    """
    with pytest.raises(PatternReferenceError):
        remove_reference(name='word')

    with pytest.raises(PatternReferenceError):
        add_reference(name='month_day', pattern=r'[a-zA-Z]{3} +\d{1,2}')
        remove_reference(name='month_day')
        remove_reference(name='month_day')
