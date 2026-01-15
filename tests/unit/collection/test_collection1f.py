import pytest       # noqa
import re
from regexapp import ElementPattern


class TestElementPatternF:

    @pytest.mark.parametrize(
        (
            'data', 'expected_pattern',
        ),
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
