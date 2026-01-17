"""
Unit tests for the `textfsmgen.collection.ElementPattern` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/collection/test_mixed_word_group_pattern_keyword.py
    or
    $ python -m pytest tests/unit/collection/test_mixed_word_group_pattern_keyword.py
"""

import pytest
from regexapp import ElementPattern


class TestMixedWordGroupPattern(object):

    @pytest.mark.parametrize(
        "data, expected_pattern",
        [
            (
                'mixed_word_group(var_meats)',
                r'(?P<meats>[\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*( +[\x21-\x7e]*[a-zA-Z0-9][\x21-\x7e]*)+)',
            ),
        ]
    )
    def test_element_pattern(self, data, expected_pattern):
        pattern = ElementPattern(data)
        assert pattern == expected_pattern
