import pytest       # noqa
from regexapp import LinePattern


class TestLinePattern:
    @pytest.mark.parametrize(
        ('user_data', 'expected_pattern'),
        [
            (
                'start() Food: word(var_food, or_empty)  Total: digits(var_total, N/A) end()',  # user prepared data
                '^Food:\\s*(?P<food>([a-zA-Z][a-zA-Z0-9]*)|) +Total: (?P<total>(\\d+)|N/A)$'        # expected_pattern
            ),
            (
                'digits(var_v1)   letters(var_v2, or_empty)     digits(var_v3)',
                '(?P<v1>\\d+)\\s*(?P<v2>([a-zA-Z]+)|) +(?P<v3>\\d+)'
            )
        ]
    )
    def test_generated_pattern(self, user_data, expected_pattern):
        pattern = LinePattern(user_data)
        assert pattern == expected_pattern
