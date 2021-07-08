import pytest
from regexapp.collection import PatternReference
from regexapp.collection import TextPattern


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