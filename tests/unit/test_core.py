import sys

import pytest
from textwrap import dedent
from regexapp import RegexBuilder
from regexapp import DynamicTestScriptBuilder
from regexapp import add_reference
from regexapp import remove_reference
from regexapp.exceptions import PatternReferenceError
from datetime import datetime
from pathlib import Path, PurePath


def is_python_v35_or_older():
    major_ver = int(sys.version_info.major)
    minor_ver = int(sys.version_info.minor)
    return major_ver == 3 and minor_ver < 6


@pytest.fixture
def tc_info():
    class TestInfo:
        pass

    test_info = TestInfo()

    ############################################################################
    # test info
    ############################################################################
    prepared_data = """
        phrase(var_subject) is digits(var_degree) degrees word(var_unit).
           IPv4 Address. . . . . . . . . . . : ipv4_address(var_ipv4_addr)(word(var_status))
    """

    test_data = """
        today temperature is 75 degrees fahrenheit.
        the highest temperature ever recorded on Earth is 134 degrees fahrenheit.
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)
    """

    test_report = """
        Test Data:
        ---------
        today temperature is 75 degrees fahrenheit.
        the highest temperature ever recorded on Earth is 134 degrees fahrenheit.
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)

        Matched Result:
        --------------
        pattern: (?P<subject>\\w+( \\w+)+) is (?P<degree>\\d+) degrees (?P<unit>\\w+)\\.
        matched: [{'subject': 'today temperature', 'degree': '75', 'unit': 'fahrenheit'}, {'subject': 'the highest temperature ever recorded on Earth', 'degree': '134', 'unit': 'fahrenheit'}]
        ----------
        pattern:  +IPv4 Address\\. \\. \\. \\. \\. \\. \\. \\. \\. \\. \\. : (?P<ipv4_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3})\\((?P<status>\\w+)\\)
        matched: [{'ipv4_addr': '192.168.0.1', 'status': 'Preferred'}]
        ----------
    """

    ############################################################################
    # other test info
    ############################################################################
    other_prepared_data = """
        file_type(var_file_type)file_permission(var_file_permission) digits(var_hard_links) word(var_file_owner) word(var_file_group)  digits(var_file_size) month_day(var_date) hour_minute(var_time) mixed_words(var_filename)
    """

    other_test_data = """
        -rw-r--r-- 1 abc 197121  133 Jun 10 20:33 README.md
        -rw-r--r-- 1 abc 197121 1488 Jul 27 00:48 setup.py
        drwxr-xr-x 1 abc 197121    0 Jul  7 15:33 tests/
    """

    other_test_report = """
        Test Data:
        ---------
        -rw-r--r-- 1 abc 197121  133 Jun 10 20:33 README.md
        -rw-r--r-- 1 abc 197121 1488 Jul 27 00:48 setup.py
        drwxr-xr-x 1 abc 197121    0 Jul  7 15:33 tests/

        Matched Result:
        --------------
        pattern: (?P<file_type>\\S)(?P<file_permission>\\S+) (?P<hard_links>\\d+) (?P<file_owner>\\w+) (?P<file_group>\\w+) +(?P<file_size>\\d+) (?P<date>[a-zA-Z]{3} +\\d{1,2}) (?P<time>\\d+:\\d+) (?P<filename>\\S*[a-zA-Z0-9]\\S*( \\S*[a-zA-Z0-9]\\S*)*)
        matched: [{'file_type': '-', 'file_permission': 'rw-r--r--', 'hard_links': '1', 'file_owner': 'abc', 'file_group': '197121', 'file_size': '133', 'date': 'Jun 10', 'time': '20:33', 'filename': 'README.md'}, {'file_type': '-', 'file_permission': 'rw-r--r--', 'hard_links': '1', 'file_owner': 'abc', 'file_group': '197121', 'file_size': '1488', 'date': 'Jul 27', 'time': '00:48', 'filename': 'setup.py'}, {'file_type': 'd', 'file_permission': 'rwxr-xr-x', 'hard_links': '1', 'file_owner': 'abc', 'file_group': '197121', 'file_size': '0', 'date': 'Jul  7', 'time': '15:33', 'filename': 'tests/'}]
        ----------
    """

    ############################################################################
    # another test info
    ############################################################################
    multiline_prepared_data = """
        I have words(var_v1).
        My friend has words(var_v2).
        I don't have words(var_v3).
    """

    multiline_test_data = """
        First line
        I have computer.
        Other line
        My friend has game console.
        Another line ....
        I don't have digital camera.
        ...
        last line
    """

    ############################################################################
    # test info - snippet scenario 1 - single pattern via line
    ############################################################################
    snippet_line_pattern_prepared_data = "word(var_v1)  digits(var_v2, or_empty)  word(var_v3, or_empty)"

    snippet_line_pattern_test_data = """
        value1   123   value2
        value3   value4
        value5   476
        value99
    """

    ############################################################################
    # test info - snippet scenario 2 - patterns via line
    ############################################################################
    snippet_line_patterns_prepared_data = """
        words(var_v1, head)   words(var_v2, tail)
        words(var_v3, head)   number(var_v4, tail)
    """

    snippet_line_patterns_test_data = """
        value1     9.99
        12.3       value 99
        value.10   value 11
        value20    value 21
        value99    N/A
    """

    ############################################################################
    # test info - snippet scenario 2 - pattern via multiline
    ############################################################################
    snippet_multiline_pattern_prepared_data = """
        words(var_subject1) live in words(var_object1).
        words(var_subject2, head) will meet words(var_object2).
    """

    snippet_multiline_pattern_test_data = """
        I live in Abc Xyz.
        My city is friendly.
        You will meet a lot of nice people.
        People enjoy fishing during weekend.
    """

    test_info.prepared_data = dedent(prepared_data).strip()
    test_info.user_data = test_info.prepared_data
    test_info.test_data = dedent(test_data).strip()
    test_info.report = dedent(test_report).strip()

    test_info.other_prepared_data = dedent(other_prepared_data).strip()
    test_info.other_user_data = test_info.other_prepared_data
    test_info.other_test_data = dedent(other_test_data).strip()
    test_info.other_report = dedent(other_test_report).strip()

    test_info.multiline_prepared_data = dedent(multiline_prepared_data).strip()
    test_info.multiline_user_data = test_info.multiline_prepared_data
    test_info.multiline_test_data = dedent(multiline_test_data).strip()

    test_info.snippet_line_pattern_prepared_data = dedent(snippet_line_pattern_prepared_data).strip()
    test_info.snippet_line_pattern_user_data = test_info.snippet_line_pattern_prepared_data
    test_info.snippet_line_pattern_test_data = dedent(snippet_line_pattern_test_data).strip()

    test_info.snippet_line_patterns_prepared_data = dedent(snippet_line_patterns_prepared_data).strip()
    test_info.snippet_line_patterns_user_data = test_info.snippet_line_patterns_prepared_data
    test_info.snippet_line_patterns_test_data = dedent(snippet_line_patterns_test_data).strip()

    test_info.snippet_multiline_pattern_prepared_data = dedent(snippet_multiline_pattern_prepared_data).strip()
    test_info.snippet_multiline_pattern_user_data = test_info.snippet_multiline_pattern_prepared_data
    test_info.snippet_multiline_pattern_test_data = dedent(snippet_multiline_pattern_test_data).strip()

    test_info.author = 'user1'
    test_info.email = 'user1@abcxyz.com'
    test_info.company = 'ABC XYZ LLC'

    dt_str = '{:%Y-%m-%d}'.format(datetime.now())

    base_dir = str(PurePath(Path(__file__).parent, 'data'))

    filename = str(PurePath(base_dir, 'unittest_script.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_unittest_script = script

    filename = str(PurePath(base_dir, 'pytest_script.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_pytest_script = script

    # multiline
    filename = str(PurePath(base_dir, 'unittest_script_for_multiline.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_unittest_script_for_multiline = script

    filename = str(PurePath(base_dir, 'pytest_script_for_multiline.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_pytest_script_for_multiline = script

    filename = str(PurePath(base_dir, 'snippet_script_for_line_pattern.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_snippet_script_for_line_pattern = script

    filename = str(PurePath(base_dir, 'snippet_script_for_line_patterns.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_snippet_script_for_line_patterns = script

    filename = str(PurePath(base_dir, 'snippet_script_for_multiline_pattern.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_snippet_script_for_multiline_pattern = script

    yield test_info


class TestRegexBuilder:
    @pytest.mark.skipif(
        is_python_v35_or_older(),
        reason='Python 3.5 dictionary is unordered hash object'
    )
    def test_regexbuilder_creation(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.user_data, test_data=tc_info.test_data,
            is_line=True
        )
        factory.build()
        factory.test()

        assert factory.test_result is True
        assert factory.test_report == tc_info.report

    def test_generating_unittest_script(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.user_data, test_data=tc_info.test_data,
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_unittest()
        assert test_script == tc_info.expected_unittest_script

    def test_generating_pytest_script(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.user_data, test_data=tc_info.test_data,
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_pytest()
        assert test_script == tc_info.expected_pytest_script

    def test_generating_unittest_script_for_multiline(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.multiline_user_data,
            test_data=tc_info.multiline_test_data,
            is_line=False,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_unittest()
        assert test_script == tc_info.expected_unittest_script_for_multiline

    def test_generating_pytest_script_for_multiline(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.multiline_user_data,
            test_data=tc_info.multiline_test_data,
            is_line=False,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_pytest()
        assert test_script == tc_info.expected_pytest_script_for_multiline

    def test_generating_python_snippet_for_line_and_pattern(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.snippet_line_pattern_user_data,
            test_data=tc_info.snippet_line_pattern_test_data,
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_python_test()
        assert test_script == tc_info.expected_snippet_script_for_line_pattern

    def test_generating_python_snippet_for_line_and_patterns(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.snippet_line_patterns_user_data,
            test_data=tc_info.snippet_line_patterns_test_data,
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_python_test()
        assert test_script == tc_info.expected_snippet_script_for_line_patterns

    def test_generating_python_snippet_for_multiline_and_pattern(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.snippet_multiline_pattern_user_data,
            test_data=tc_info.snippet_multiline_pattern_test_data,
            is_line=False,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_python_test()
        assert test_script == tc_info.expected_snippet_script_for_multiline_pattern


@pytest.mark.skipif(
    is_python_v35_or_older(),
    reason='Python 3.5 dictionary is unordered hash object'
)
def test_add_reference(tc_info):
    add_reference(name='file_type', pattern=r'\S')
    add_reference(name='file_permission', pattern=r'\S+')
    add_reference(name='month_day', pattern=r'[a-zA-Z]{3} +\d{1,2}')
    add_reference(name='hour_minute', pattern=r'\d+:\d+')

    factory = RegexBuilder(
        user_data=tc_info.other_user_data, test_data=tc_info.other_test_data,
        is_line=True
    )
    factory.build()
    factory.test()
    assert factory.test_result is True
    assert factory.test_report == tc_info.other_report


def test_remove_reference():
    add_reference(name='month_day', pattern=r'[a-zA-Z]{3} +\d{1,2}')
    remove_reference(name='month_day')


def test_add_reference_exception():
    with pytest.raises(PatternReferenceError):
        remove_reference(name='word')

    with pytest.raises(PatternReferenceError):
        add_reference(name='month_day', pattern=r'[a-zA-Z]{3} +\d{1,2}')
        remove_reference(name='month_day')
        remove_reference(name='month_day')


class TestDynamicGenTestScript:
    def test_generating_unittest_script(self, tc_info):
        factory = DynamicTestScriptBuilder(
            test_info=[tc_info.prepared_data, tc_info.test_data],
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_unittest()
        assert test_script == tc_info.expected_unittest_script

    def test_generating_pytest_script(self, tc_info):
        factory = DynamicTestScriptBuilder(
            test_info=[tc_info.prepared_data, tc_info.test_data],
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
            filename='tc.txt'
        )
        test_script = factory.create_pytest()
        assert test_script == tc_info.expected_pytest_script

    # multi-lines tests
    def test_generating_unittest_script_for_multiline(self, tc_info):
        factory = DynamicTestScriptBuilder(
            test_info=[
                tc_info.multiline_prepared_data,
                tc_info.multiline_test_data
            ],
            is_line=False,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_unittest()
        assert test_script == tc_info.expected_unittest_script_for_multiline

    def test_generating_pytest_script_for_multiline(self, tc_info):
        factory = DynamicTestScriptBuilder(
            test_info=[
                tc_info.multiline_prepared_data,
                tc_info.multiline_test_data
            ],
            is_line=False,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_pytest()
        assert test_script == tc_info.expected_pytest_script_for_multiline

    def test_generating_python_snippet_for_line_and_pattern(self, tc_info):
        factory = DynamicTestScriptBuilder(
            test_info=[
                tc_info.snippet_line_pattern_prepared_data,
                tc_info.snippet_line_pattern_test_data
            ],
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_python_test()
        assert test_script == tc_info.expected_snippet_script_for_line_pattern

    def test_generating_python_snippet_for_line_and_patterns(self, tc_info):
        factory = DynamicTestScriptBuilder(
            test_info=[
                tc_info.snippet_line_patterns_prepared_data,
                tc_info.snippet_line_patterns_test_data
            ],
            is_line=True,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_python_test()
        assert test_script == tc_info.expected_snippet_script_for_line_patterns

    def test_generating_python_snippet_for_multiline_and_pattern(self, tc_info):
        factory = DynamicTestScriptBuilder(
            test_info=[
                tc_info.snippet_multiline_pattern_prepared_data,
                tc_info.snippet_multiline_pattern_test_data
            ],
            is_line=False,
            author=tc_info.author,
            email=tc_info.email,
            company=tc_info.company,
        )
        test_script = factory.create_python_test()
        assert test_script == tc_info.expected_snippet_script_for_multiline_pattern
