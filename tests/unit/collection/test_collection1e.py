import pytest       # noqa
import re
from regexapp import ElementPattern


class TestElementPatternE:

    @pytest.mark.parametrize(
        (
            'data', 'expected_pattern', 'expected_pattern_after_removed'
        ),
        [
            (
                'words(head)',
                '^[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*',
                '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*'
            ),
            (
                'words(var_v1, head_whitespace)',
                '^\\s*(?P<v1>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)',
                '(?P<v1>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)'
            ),
        ]
    )
    def test_remove_head_of_pattern(self, data, expected_pattern,
                                    expected_pattern_after_removed):
        pattern = ElementPattern(data)
        assert pattern == expected_pattern

        removed_head_of_str_pattern = pattern.remove_head_of_string()
        assert removed_head_of_str_pattern == expected_pattern_after_removed

    @pytest.mark.parametrize(
        (
            'data', 'expected_pattern', 'expected_pattern_after_removed'
        ),
        [
            (
                'words(tail)',
                '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*$',
                '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*'
            ),
            (
                'words(var_v1, tail_whitespace)',
                '(?P<v1>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)\\s*$',
                '(?P<v1>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)'
            ),
        ]
    )
    def test_remove_tail_of_pattern(self, data, expected_pattern,
                                    expected_pattern_after_removed):
        pattern = ElementPattern(data)
        assert pattern == expected_pattern

        removed_tail_of_str_pattern = pattern.remove_tail_of_string()
        assert removed_tail_of_str_pattern == expected_pattern_after_removed
