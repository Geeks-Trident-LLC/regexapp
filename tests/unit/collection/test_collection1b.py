import pytest       # noqa
import re
from regexapp import ElementPattern


class TestElementPattern:
    @pytest.mark.parametrize(
        ('data', 'expected_result'),
        [
            ####################################################################
            # alternative or_ for repeating or occurring space                 #
            ####################################################################
            ('word(var_v1, or_repeating_5_space)', '(?P<v1>( {5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_repeat_5_spaces)', '(?P<v1>( {5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_repeats_5_spaces)', '(?P<v1>( {5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_5_spaces)', '(?P<v1>( {5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_5_occurrences_spaces)', '(?P<v1>( {5})|([a-zA-Z][a-zA-Z0-9]*))'),

            ('word(var_v1, or_repeating_2_5_spaces)', '(?P<v1>( {2,5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_repeat_2_5_spaces)', '(?P<v1>( {2,5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_repeats_2_5_spaces)', '(?P<v1>( {2,5})|([a-zA-Z][a-zA-Z0-9]*))'),

            ('word(var_v1, or_repeating__5_spaces)', '(?P<v1>( {,5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_repeat__5_spaces)', '(?P<v1>( {,5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_repeats__5_spaces)', '(?P<v1>( {,5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_at_most_5_spaces)', '(?P<v1>( {,5})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_at_most_5_occurrences_spaces)', '(?P<v1>( {,5})|([a-zA-Z][a-zA-Z0-9]*))'),

            ('word(var_v1, or_repeat_5__spaces)', '(?P<v1>( {5,})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_at_least_5_spaces)', '(?P<v1>( {5,})|([a-zA-Z][a-zA-Z0-9]*))'),
            ('word(var_v1, or_at_least_5_occurrences_spaces)', '(?P<v1>( {5,})|([a-zA-Z][a-zA-Z0-9]*))'),

            ('word(var_v1, or_either_5_spaces)', '(?P<v1>( {5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
            ('word(var_v1, or_either_repeat_5_spaces)', '(?P<v1>( {5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),

            ('word(var_v1, or_either_repeating_2_5_spaces)', '(?P<v1>( {2,5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
            ('word(var_v1, or_either_repeat_2_5_spaces)', '(?P<v1>( {2,5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
            ('word(var_v1, or_either_repeating_2_5_spaces)', '(?P<v1>( {2,5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),

            ('word(var_v1, or_either_repeat_5__spaces)', '(?P<v1>( {5,})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
            ('word(var_v1, or_either_at_least_5_occurrences_spaces)', '(?P<v1>( {5,})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
            ('word(var_v1, or_either_at_least_5_spaces)', '(?P<v1>( {5,})|( *[a-zA-Z][a-zA-Z0-9]* *))'),

            ('word(var_v1, or_either_repeat__5_spaces)', '(?P<v1>( {,5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
            ('word(var_v1, or_either_at_most_5_spaces)', '(?P<v1>( {,5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
            ('word(var_v1, or_either_at_most_5_occurrences_spaces)', '(?P<v1>( {,5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),

            ('word(var_v1, or_either_5_occurrences_spaces)', '(?P<v1>( {5})|( *[a-zA-Z][a-zA-Z0-9]* *))'),
        ]
    )
    def test_element_pattern(self, data, expected_result):
        pattern = ElementPattern(data)
        assert pattern == expected_result
        try:
            re.compile(pattern)
        except Exception as ex:
            error = 'invalid pattern: %r (err-msg: %s)' % (pattern, ex)
            assert False, error
