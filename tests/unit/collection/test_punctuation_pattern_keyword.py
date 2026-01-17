"""
Unit tests for the `textfsmgen.collection.ElementPattern` class.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/collection/test_punctuation_pattern_keyword.py
    or
    $ python -m pytest tests/unit/collection/test_punctuation_pattern_keyword.py
"""

from regexapp import ElementPattern
import string
import re


class TestPunctuationPattern:
    def test_punctuation_pattern(self):
        pattern = ElementPattern('punctuation()')
        for p_char in string.punctuation:
            assert re.match(f'{pattern}$', p_char)

    def test_punctuations_pattern(self):
        pattern = ElementPattern('punctuations()')
        for p_char in string.punctuation:
            assert re.match(f'{pattern}$', p_char)

    def test_graph_pattern(self):
        pattern = ElementPattern('graph()')
        for i in range(256):
            c = chr(i)
            match = re.match(pattern, c)
            if 33 <= i <= 126:
                assert bool(match)
            else:
                if match:
                    assert False

    def test_non_punctuation_pattern(self):
        pattern = ElementPattern('non_punctuation()')
        for i in range(256):
            c = chr(i)
            match = re.match(pattern, c)
            if c in string.punctuation:
                assert not bool(match)
            else:
                assert bool(match)