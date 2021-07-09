import pytest
import re
from regexapp.collection import PatternReference
from regexapp.collection import TextPattern
from regexapp.collection import ElementPattern
from regexapp.collection import LinePattern


class TestPatternReference:
    def test_initialization(self):
        obj = PatternReference()
        assert obj.get('word').get('pattern') == r'\w+'


class TestTextPattern:
    @pytest.mark.parametrize(
        "data,used_space,expected_result",
        [
            ('first last', True, 'first +last'),
            ('first last', False, 'first\\s+last'),
            ('Keepalive set (10 sec)', True, 'Keepalive +set +\\(10 +sec\\)'),
            ('Keepalive set (10 sec)', False, 'Keepalive\\s+set\\s+\\(10\\s+sec\\)'),
        ]
    )
    def test_text_pattern(self, data, used_space, expected_result):
        text_pat = TextPattern(data, used_space=used_space)
        assert text_pat == expected_result


class TestElementPattern:
    @pytest.mark.parametrize(
        "data,expected_result",
        [
            ####################################################################
            # predefined keyword test                                          #
            ####################################################################
            ('whitespace()', '\\s+'),
            ('notwhitespace()', '\\S+'),
            ('letter()', '[a-zA-Z]'),
            ('letters()', '[a-zA-Z]+'),
            ('word()', '\\w+'),
            ('words()', '\\w+(\\s+\\w+)*'),
            ('mixed_word()', '\\S*[a-zA-Z0-9]\\S*'),
            ('mixed_words()', '\\S*[a-zA-Z0-9]\\S*(\\s+\\S*[a-zA-Z0-9]\\S*)*'),
            ('phrase()', '\\w+(\\s+\\w+)+'),
            ('mixed_phrase()', '\\S*[a-zA-Z0-9]\\S*(\\s+\\S*[a-zA-Z0-9]\\S*)+'),
            ('digit()', '\\d'),
            ('digits()', '\\d+'),
            ('number()', '(\\d+)?[.]?\\d+'),
            ('signed_number()', '[+(-]?(\\d+)?[.]?\\d+[)]?'),
            ('mixed_number()', '[+\\(\\[\\$-]?(\\d+(,\\d+)*)?[.]?\\d+[\\]\\)%a-zA-Z]*'),
            ####################################################################
            # predefined keyword test combining with other flags               #
            ####################################################################
            ('word(var_v1, or_empty)', '(?P<v1>\\w+|)'),
            ('word(var_v1, or_n/a, or_empty)', '(?P<v1>\\w+|n/a|)'),
            ('word(var_v1, or_abc xyz, or_12.95 19.95, or_empty)', '(?P<v1>\\w+|(abc xyz)|(12.95 19.95)|)'),
            ####################################################################
            # choice keyword test                                              #
            ####################################################################
            ('choice(up, down, administratively down)', 'up|down|(administratively down)'),
            ('choice(up, down, administratively down, var_v2)', '(?P<v2>up|down|(administratively down))'),
            ####################################################################
            # raw data test                                                    #
            ####################################################################
            ('word(raw>>>)', 'word\\(\\)'),
            ('word(raw>>>data="")', 'word\\(data=""\\)'),
            ####################################################################
            # unknown keyword test                                             #
            ####################################################################
            ('abc_word()', 'abc_word\\(\\)'),
            ('xyz_word()', 'xyz_word\\(\\)'),
        ]
    )
    def test_element_pattern(self, data, expected_result):
        pattern = ElementPattern(data)
        assert pattern == expected_result


class TestLinePattern:
    @pytest.mark.parametrize(
        "test_data,user_prepared_data,expected_pattern,used_space,prepended_ws,appended_ws,ignore_case",
        [
            (
                ' \t\n\r\f\v',      # test data
                ' ',                # user prepared data
                '^\\s*$',           # expected pattern
                True, False, False, True,
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '\\S*[a-zA-Z0-9]\\S*\\s+is\\s+up|down|(administratively down),\\s+line\\s+protocol\\s+is\\s+up|down|(administratively down)',   # expected pattern
                False, False, False, False,
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down)',               # expected pattern
                True, False, False, False,
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '(?i)\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down)',           # expected pattern
                True, False, False, True,
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '(?i)^ *\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down)',        # expected pattern
                True, True, False, True,
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '(?i)^ *\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down) *$',     # expected pattern
                True, True, True, True,
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                                                                                          # test data
                'mixed_word(var_interface_name) is choice(up, down, administratively down, var_interface_status), line protocol is choice(up, down, administratively down, var_protocol_status)',           # user prepared data
                '(?i)^ *(?P<interface_name>\\S*[a-zA-Z0-9]\\S*) +is +(?P<interface_status>up|down|(administratively down)), +line +protocol +is +(?P<protocol_status>up|down|(administratively down)) *$',  # expected pattern
                True, True, True, True,
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                                                      # test data
                'mixed_word(var_interface_name) is words(var_interface_status), line protocol is words(var_protocol_status)',                                           # user prepared data
                '(?i)(?P<interface_name>\\S*[a-zA-Z0-9]\\S*) +is +(?P<interface_status>\\w+(\\s+\\w+)*), +line +protocol +is +(?P<protocol_status>\\w+(\\s+\\w+)*)',    # expected pattern
                True, False, False, True,
            ),
        ]
    )
    def test_line_pattern(self, test_data, user_prepared_data,expected_pattern,
                          used_space, prepended_ws, appended_ws, ignore_case):
        pattern = LinePattern(
            user_prepared_data, used_space=used_space,
            prepended_ws=prepended_ws, appended_ws=appended_ws,
            ignore_case=ignore_case
        )
        assert pattern == expected_pattern
        match = re.search(pattern, test_data)
        assert match is not None