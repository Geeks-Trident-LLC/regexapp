import pytest       # noqa
import re
from textwrap import dedent

from regexapp import LinePattern
from regexapp import PatternBuilder
from regexapp import MultilinePattern


class TestPatternBuilder:
    @pytest.mark.parametrize(
        ('test_data', 'expected_pattern', 'var_name', 'word_bound'),
        [
            (
                ['Friday, April  9, 2021 8:43:15 PM'],
                '[a-zA-Z]+, [a-zA-Z]+ +[0-9]+, [0-9]+ [0-9]+:[0-9]+:[0-9]+ [a-zA-Z]+',
                '',     # var_name
                '',     # word_bound

            ),
            (
                [
                    'Friday, April  9, 2021 8:43:15 PM',
                    '12/06/2010 08:56:45'
                ],
                '(([a-zA-Z]+, [a-zA-Z]+ +[0-9]+, [0-9]+ [0-9]+:[0-9]+:[0-9]+ [a-zA-Z]+)|([0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9]+:[0-9]+))',      # noqa
                '',     # var_name
                '',     # word_bound
            ),
            (
                ['2019 Dec  8 14:44:01'],
                '[0-9]+ [a-zA-Z]+ +[0-9]+ [0-9]+:[0-9]+:[0-9]+',
                '',     # var_name
                '',     # word_bound
            ),
            (
                ['2019 Dec  8 14:44:01'],
                '(?P<datetime>[0-9]+ [a-zA-Z]+ +[0-9]+ [0-9]+:[0-9]+:[0-9]+)',
                'datetime',     # var_name
                '',             # word_bound
            ),
            (
                ['2019 Dec  8 14:44:01'],
                '(?P<datetime>\\b([0-9]+ [a-zA-Z]+ +[0-9]+ [0-9]+:[0-9]+:[0-9]+))',
                'datetime',  # var_name
                'word_bound_left',  # word_bound
            ),
            (
                ['2019 Dec  8 14:44:01'],
                '(?P<datetime>([0-9]+ [a-zA-Z]+ +[0-9]+ [0-9]+:[0-9]+:[0-9]+)\\b)',
                'datetime',  # var_name
                'word_bound_right',     # word_bound
            ),
            (
                ['2019 Dec  8 14:44:01'],
                '(?P<datetime>\\b([0-9]+ [a-zA-Z]+ +[0-9]+ [0-9]+:[0-9]+:[0-9]+)\\b)',
                'datetime',  # var_name
                'word_bound',   # word_bound
            ),

        ]
    )
    def test_pattern_builder(self, test_data, expected_pattern, var_name, word_bound):
        pattern = PatternBuilder(test_data, var_name=var_name, word_bound=word_bound)
        assert pattern == expected_pattern
        for data in test_data:
            match = re.search(pattern, data)
            assert match is not None


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
        first line
        today temperature is 75 degrees fahrenheit.
        other line
        another line
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)
        last line
    """

    expected_matched_text = """
        today temperature is 75 degrees fahrenheit.
        other line
        another line
           IPv4 Address. . . . . . . . . . . : 192.168.0.1(Preferred)
    """
    expected_matched_vars = dict(
        subject='today temperature',
        degree='75',
        unit='fahrenheit',
        ipv4_addr='192.168.0.1',
        status='Preferred'
    )

    test_info.prepared_data = dedent(prepared_data).strip()
    test_info.user_data = test_info.prepared_data
    test_info.test_data = dedent(test_data).strip()
    test_info.expected_matched_text = dedent(expected_matched_text).strip()
    test_info.expected_matched_vars = expected_matched_vars

    yield test_info


class TestMultilinePattern:
    def test_multiline_pattern(self, tc_info):
        multiline_pat = MultilinePattern(tc_info.prepared_data, ignore_case=False)

        match = re.search(multiline_pat, tc_info.test_data)
        matched_txt = match.group()
        matched_vars = match.groupdict()

        assert matched_txt == tc_info.expected_matched_text
        assert matched_vars == tc_info.expected_matched_vars

        multiline_pat = MultilinePattern(tc_info.prepared_data, ignore_case=True)

        match = re.search(multiline_pat, tc_info.test_data)
        matched_txt = match.group()
        matched_vars = match.groupdict()

        assert matched_txt == tc_info.expected_matched_text
        assert matched_vars == tc_info.expected_matched_vars
