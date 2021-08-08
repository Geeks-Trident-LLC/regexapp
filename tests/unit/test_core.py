import sys

import pytest
from textwrap import dedent
from regexapp import RegexBuilder
from regexapp import DynamicGenTestScript
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
        pattern: (?P<subject>\\w+( +\\w+)+) +is +(?P<degree>\\d+) +degrees +(?P<unit>\\w+)\\.
        matched: [{'subject': 'today temperature', 'degree': '75', 'unit': 'fahrenheit'}, {'subject': 'the highest temperature ever recorded on Earth', 'degree': '134', 'unit': 'fahrenheit'}]
        ----------
        pattern:  +IPv4 +Address\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +: +(?P<ipv4_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3})\\((?P<status>\\w+)\\)
        matched: [{'ipv4_addr': '192.168.0.1', 'status': 'Preferred'}]
        ----------
    """

    ############################################################################
    # other test info
    ############################################################################
    other_prepared_data = """
        file_type(var_file_type)file_permission(var_file_permission) digits(var_hard_links) word(var_file_owner) word(var_file_group) digits(var_file_size) month_day(var_date) hour_minute(var_time) mixed_words(var_filename)
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
        pattern: (?P<file_type>\\S)(?P<file_permission>\\S+) +(?P<hard_links>\\d+) +(?P<file_owner>\\w+) +(?P<file_group>\\w+) +(?P<file_size>\\d+) +(?P<date>[a-zA-Z]{3} +\\d{1,2}) +(?P<time>\\d+:\\d+) +(?P<filename>\\S*[a-zA-Z0-9]\\S*( +\\S*[a-zA-Z0-9]\\S*)*)
        matched: [{'file_type': '-', 'file_permission': 'rw-r--r--', 'hard_links': '1', 'file_owner': 'abc', 'file_group': '197121', 'file_size': '133', 'date': 'Jun 10', 'time': '20:33', 'filename': 'README.md'}, {'file_type': '-', 'file_permission': 'rw-r--r--', 'hard_links': '1', 'file_owner': 'abc', 'file_group': '197121', 'file_size': '1488', 'date': 'Jul 27', 'time': '00:48', 'filename': 'setup.py'}, {'file_type': 'd', 'file_permission': 'rwxr-xr-x', 'hard_links': '1', 'file_owner': 'abc', 'file_group': '197121', 'file_size': '0', 'date': 'Jul  7', 'time': '15:33', 'filename': 'tests/'}]
        ----------
    """

    test_info.prepared_data = dedent(prepared_data).strip()
    test_info.user_data = test_info.prepared_data
    test_info.test_data = dedent(test_data).strip()
    test_info.report = dedent(test_report).strip()

    test_info.other_prepared_data = dedent(other_prepared_data).strip()
    test_info.other_user_data = test_info.other_prepared_data
    test_info.other_test_data = dedent(other_test_data).strip()
    test_info.other_report = dedent(other_test_report).strip()

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

    filename = str(PurePath(base_dir, 'detail_unittest_script.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_detail_unittest_script = script

    filename = str(PurePath(base_dir, 'pytest_script.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_pytest_script = script

    filename = str(PurePath(base_dir, 'detail_pytest_script.txt'))
    with open(filename) as stream:
        script = stream.read()
        script = script.replace('_datetime_', dt_str)
        test_info.expected_detail_pytest_script = script

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
            is_line=True
        )
        test_script = factory.generate_unittest(author=tc_info.author,
                                                email=tc_info.email,
                                                company=tc_info.company,
                                                is_minimal=True,)
        assert test_script == tc_info.expected_unittest_script

    def test_generating_detail_unittest_script(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.user_data, test_data=tc_info.test_data,
            is_line=True
        )
        test_script = factory.generate_unittest(author=tc_info.author,
                                                email=tc_info.email,
                                                company=tc_info.company,
                                                is_minimal=False,)
        assert test_script == tc_info.expected_detail_unittest_script

    def test_generating_pytest_script(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.user_data, test_data=tc_info.test_data,
            is_line=True
        )
        test_script = factory.generate_pytest(author=tc_info.author,
                                              email=tc_info.email,
                                              company=tc_info.company,
                                              is_minimal=True,)
        assert test_script == tc_info.expected_pytest_script

    def test_generating_detail_pytest_script(self, tc_info):
        factory = RegexBuilder(
            user_data=tc_info.user_data, test_data=tc_info.test_data,
            is_line=True
        )
        test_script = factory.generate_pytest(author=tc_info.author,
                                              email=tc_info.email,
                                              company=tc_info.company,
                                              is_minimal=False,)
        assert test_script == tc_info.expected_detail_pytest_script


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
        factory = DynamicGenTestScript(
            test_info=[tc_info.prepared_data, tc_info.test_data],
            is_line=True
        )
        test_script = factory.generate_unittest(author=tc_info.author,
                                                email=tc_info.email,
                                                company=tc_info.company,
                                                is_minimal=True,)
        assert test_script == tc_info.expected_unittest_script

    def test_generating_detail_unittest_script(self, tc_info):
        factory = DynamicGenTestScript(
            test_info=[tc_info.prepared_data, tc_info.test_data],
            is_line=True
        )
        test_script = factory.generate_unittest(author=tc_info.author,
                                                email=tc_info.email,
                                                company=tc_info.company,
                                                is_minimal=False)
        assert test_script == tc_info.expected_detail_unittest_script

    def test_generating_pytest_script(self, tc_info):
        factory = DynamicGenTestScript(
            test_info=[tc_info.prepared_data, tc_info.test_data],
            is_line=True
        )
        test_script = factory.generate_pytest(author=tc_info.author,
                                              email=tc_info.email,
                                              company=tc_info.company,
                                              is_minimal=True,)
        assert test_script == tc_info.expected_pytest_script

    def test_generating_detail_pytest_script(self, tc_info):
        factory = DynamicGenTestScript(
            test_info=[tc_info.prepared_data, tc_info.test_data],
            is_line=True
        )
        test_script = factory.generate_pytest(author=tc_info.author,
                                              email=tc_info.email,
                                              company=tc_info.company,
                                              is_minimal=False)
        assert test_script == tc_info.expected_detail_pytest_script
