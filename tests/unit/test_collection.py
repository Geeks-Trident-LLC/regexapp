import pytest
from regexapp.collection import PatternReference
from regexapp.collection import TextPattern
from regexapp.collection import ElementPattern


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
    def test_text_pattern(self, data, expected_result):
        pattern = ElementPattern(data)
        assert pattern == expected_result