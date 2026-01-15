import pytest       # noqa

from regexapp import PatternReference
from regexapp import TextPattern


class TestPatternReference:
    def test_initialization(self):
        obj = PatternReference()
        assert obj.get('word').get('pattern') == r'[a-zA-Z][a-zA-Z0-9]*'


class TestTextPattern:
    @pytest.mark.parametrize(
        ('data', 'expected_result'),
        [
            ('first last', 'first last'),
            ('first\tlast', 'first\\slast'),
            ('first\nlast', 'first[\\r\\n]{1,2}last'),
            ('first\r\nlast', 'first[\\r\\n]{1,2}last'),
            ('first   last   fullname', 'first +last +fullname'),
            (' first   last   fullname', ' first +last +fullname'),
            ('  first   last   fullname', ' +first +last +fullname'),
            ('\nfirst   last   fullname', '[\\r\\n]{1,2}first +last +fullname'),
            ('\n first   last   fullname', '[\\r\\n]{1,2} first +last +fullname')
        ]
    )
    def test_text_pattern(self, data, expected_result):
        text_pat = TextPattern(data)
        assert text_pat == expected_result

    def test_pattern_is_empty(self):
        text_pat = TextPattern('')
        is_empty = text_pat.is_empty
        assert is_empty

    def test_pattern_is_empty_or_whitespace(self):
        for data in ['', ' ']:
            text_pat = TextPattern(data)
            chk = text_pat.is_empty_or_whitespace
            assert chk

            text_pat = TextPattern(data)
            chk = text_pat.is_empty_or_whitespace
            assert chk

    def test_pattern_is_whitespace(self):
        data = ' '
        text_pat = TextPattern(data)
        chk = text_pat.is_empty_or_whitespace
        assert chk

        text_pat = TextPattern(data)
        chk = text_pat.is_empty_or_whitespace
        assert chk

    @pytest.mark.parametrize(
        ('data', 'chars', 'expected_result'),
        [
            ('  abc  123  xyz  ', None, 'abc +123 +xyz +'),
            ('  abc  123  xyz  ', ' a', 'bc +123 +xyz +'),
            ('  abc  123  xyz  abc  ', ' abc', '123 +xyz +abc +'),
        ]
    )
    def test_lstrip(self, data, chars, expected_result):
        text_pat = TextPattern(data)
        result = text_pat.lstrip(chars=chars)
        assert result == expected_result

    @pytest.mark.parametrize(
        ('data', 'chars', 'expected_result'),
        [
            ('  abc  123  xyz  ', None, ' +abc +123 +xyz'),
            ('  abc  123  xyz  ', ' z', ' +abc +123 +xy'),
            ('  abc  123  xyz  ', ' xyz', ' +abc +123'),
        ]
    )
    def test_lstrip(self, data, chars, expected_result):
        text_pat = TextPattern(data)
        result = text_pat.rstrip(chars=chars)
        assert result == expected_result

    @pytest.mark.parametrize(
        ('data', 'chars', 'expected_result'),
        [
            ('  abc  123  xyz  ', None, 'abc +123 +xyz'),
            ('  abc  123  xyz  ', ' a', 'bc +123 +xyz'),
            ('  abc  123  xyz  ', ' abc', '123 +xyz'),
            ('  abc  123  xyz  ', ' abcxyz', '123'),
        ]
    )
    def test_strip(self, data, chars, expected_result):
        text_pat = TextPattern(data)
        result = text_pat.strip(chars=chars)
        assert result == expected_result

    @pytest.mark.parametrize(
        ('data', 'other', 'as_is', 'expected_result'),
        [
            ('a', 'b', True, 'ab'),
            ('a', '*', True, 'a*'),
            ('a ', '+ b', False, 'a \\+ b'),
            ('a ', TextPattern('+ b'), False, 'a \\+ b'),
            ('a ', TextPattern('+ b'), True, 'a \\+ b'),
            ('a', ['(b', 'c)', '*'], True, 'a(bc)*'),
        ]
    )
    def test_add(self, data, other, as_is, expected_result):
        text_pat = TextPattern(data)
        result = text_pat.add(other, as_is=as_is)
        assert result == expected_result

    @pytest.mark.parametrize(
        ('data', 'other', 'as_is', 'expected_result'),
        [
            ('a', 'b', True, 'ab'),
            ('a', '*', True, 'a*'),
            ('a ', '+ b', False, 'a \\+ b'),
            ('a ', TextPattern('+ b'), False, 'a \\+ b'),
            ('a ', TextPattern('+ b'), True, 'a \\+ b'),
            ('a', ['(b', 'c)', '*'], True, 'a(bc)*'),
            ('a', ['(', ('b', 'c'), ')', '*'], True, 'a(bc)*'),
        ]
    )
    def test_add(self, data, other, as_is, expected_result):
        text_pat = TextPattern(data)
        if isinstance(other, (list, tuple)):
            result = text_pat.concatenate(*other, as_is=as_is)
        else:
            result = text_pat.concatenate(other, as_is=as_is)
        assert result == expected_result
