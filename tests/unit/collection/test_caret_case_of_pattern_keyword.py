"""
Unit tests for the `textfsmgen.collection.ElementPattern` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/collection/test_caret_case_of_pattern_keyword.py
    or
    $ python -m pytest tests/unit/collection/test_caret_case_of_pattern_keyword.py
"""

import pytest
from regexapp import ElementPattern


class TestCaretOfPatternKeyword:

    @pytest.mark.parametrize(
        "data, expected_pattern, expected_pattern_after_removed",
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
        "data, expected_pattern, expected_pattern_after_removed",
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
