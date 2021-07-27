import pytest
from textwrap import dedent
from regexapp import RegexBuilder


@pytest.fixture
def user_data():
    prepared_data = """
        phrase(var_subject) is digits(var_degree) degrees word(var_unit).
           IPv4 Address. . . . . . . . . . . : ipv4_address(var_ipv4_addr)(word(var_status))
    """
    yield dedent(prepared_data).strip()


@pytest.fixture
def test_data():
    test_data = """
        today temperature is 75 degrees fahrenheit.
        the highest temperature ever recorded on Earth is 134 degrees fahrenheit.
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)
    """
    yield dedent(test_data).strip()


@pytest.fixture
def report():
    test_report = """
        Test Data:
        ---------
        today temperature is 75 degrees fahrenheit.
        the highest temperature ever recorded on Earth is 134 degrees fahrenheit.
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)
        
        Matched Result:
        --------------
        pattern: (?P<subject>\\w+(\\s+\\w+)+) +is +(?P<degree>\\d+) +degrees +(?P<unit>\\w+)\\.
        matched: [{'subject': 'today temperature', 'degree': '75', 'unit': 'fahrenheit'}, {'subject': 'the highest temperature ever recorded on Earth', 'degree': '134', 'unit': 'fahrenheit'}]
        ----------
        pattern:  +IPv4 +Address\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +: +(?P<ipv4_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3})\\((?P<status>\\w+)\\)
        matched: [{'ipv4_addr': '192.168.0.1', 'status': 'Preferred'}]
        ----------
    """
    yield dedent(test_report).strip()


def test_regex_builder(user_data, test_data, report):
    obj = RegexBuilder(user_data=user_data, test_data=test_data)
    obj.build()
    obj.test()
    assert obj.test_result is True
    assert obj.test_report == report
