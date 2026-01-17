"""
Unit tests for the `textfsmgen.config` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/collection/test_or_empty_flag_for_pattern_keyword.py
    or
    $ python -m pytest tests/unit/collection/test_or_empty_flag_for_pattern_keyword.py
"""

import pytest
from regexapp import ElementPattern
from regexapp import LinePattern


class TestOrEmptyFlagForPatternKeyword:
    @pytest.mark.parametrize(
        "user_data, expected_pattern",
        [
            ('data(abc, or_empty)', '(abc|)'),
            ('data(var_v1, abc, or_empty)', '(?P<v1>abc|)'),

            ('letter(or_empty)', r'(([a-zA-Z])|)'),
            ('letter(var_v1, or_empty)', r'(?P<v1>([a-zA-Z])|)'),

            ('digit(or_empty)', r'((\d)|)'),
            ('digit(var_v1, or_empty)', r'(?P<v1>(\d)|)'),

            ('number(or_empty)', r'((\d*[.]?\d+)|)'),
            ('number(var_v1, or_empty)', r'(?P<v1>(\d*[.]?\d+)|)'),

            ('mixed_number(or_empty)', r'(([+\(\[\$-]?(\d+([,:/-]\d+)*)?[.]?\d+[\]\)%a-zA-Z]*)|)'),
            ('mixed_number(var_v1, or_empty)', r'(?P<v1>([+\(\[\$-]?(\d+([,:/-]\d+)*)?[.]?\d+[\]\)%a-zA-Z]*)|)'),

            ('punct(or_empty)', r'(([\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e])|)'),
            ('punct(var_v1, or_empty)', r'(?P<v1>([\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e])|)'),
            (
                'puncts_or_phrase(var_v1, or_empty)',
                r'(?P<v1>(([\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+( [\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+)*))|)'
            ),

            ('word(or_empty)', r'(([a-zA-Z][a-zA-Z0-9]*)|)'),
            ('word(var_v1, or_empty)', r'(?P<v1>([a-zA-Z][a-zA-Z0-9]*)|)'),
            ('words(var_v1, or_empty)', r'(?P<v1>(([a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*))|)'),

            ('mixed_word(or_empty)', r'(([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)|)'),
            ('mixed_word(var_v1, or_empty)', r'(?P<v1>([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)|)'),
            (
                'mixed_words(var_v1, or_empty)',
                r'(?P<v1>(([\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( [\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)*))|)'),

            ('non_whitespaces(or_empty)', r'((\S+)|)'),
            ('non_whitespaces(var_v1, or_empty)', r'(?P<v1>(\S+)|)'),
            ('non_whitespaces_group(var_v1, or_empty)', r'(?P<v1>((\S+( +\S+)+))|)'),

        ]
    )
    def test_element_pattern(self, user_data, expected_pattern):
        pattern = ElementPattern(user_data)
        assert pattern == expected_pattern


class TestLineArgumentOrEmpty:
    @pytest.mark.parametrize(
        "user_data, expected_pattern",
        [
            ('blab data(var_v1, abc, or_empty) blab', r'blab\s*(?P<v1>abc|) blab'),
            (
                'blab data(var_v1, abc, or_empty) data(var_v2, xyz, or_empty) blab',
                r'blab\s*(?P<v1>abc|)\s*(?P<v2>xyz|) blab'
            ),
            (
                'blab data(var_v1, abc, or_empty) ++blab-- data(var_v2, xyz, or_empty) blab',
                r'blab\s*(?P<v1>abc|) \+\+blab--\s*(?P<v2>xyz|) blab'
            ),
        ]
    )
    def test_element_pattern(self, user_data, expected_pattern):
        pattern = LinePattern(user_data)
        assert pattern == expected_pattern
