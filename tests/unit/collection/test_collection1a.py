import pytest       # noqa
import re
from regexapp import ElementPattern


class TestElementPatternA:
    @pytest.mark.parametrize(
        ('data', 'expected_result'),
        [
            ####################################################################
            # predefined keyword test combining with other flags               #
            ####################################################################
            ('word(var_v1, or_empty)', '(?P<v1>([a-zA-Z][a-zA-Z0-9]*)|)'),
            ('word(var_v1, or_n/a, or_empty)', '(?P<v1>(([a-zA-Z][a-zA-Z0-9]*)|n/a)|)'),
            ('word(var_v1, or_abc xyz, or_12.95 19.95, or_empty)', '(?P<v1>(([a-zA-Z][a-zA-Z0-9]*)|(abc xyz)|(12.95 19.95))|)'),
            ('word(var_v1, word_bound_left)', '(?P<v1>\\b[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, word_bound_right)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*\\b)'),
            ('word(var_v1, word_bound)', '(?P<v1>\\b[a-zA-Z][a-zA-Z0-9]*\\b)'),
            ('word(var_v1, word_bound_raw)', '(?P<v1>([a-zA-Z][a-zA-Z0-9]*)|word_bound)'),
            ('word(var_v1, head)', '^(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_ws)', '^\\s*(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_ws_plus)', '^\\s+(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_whitespace)', '^\\s*(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_whitespace_plus)', '^\\s+(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_whitespaces)', '^\\s+(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_space)', '^ *(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_space_plus)', '^ +(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_spaces)', '^ +(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_ws)', '\\s*(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_ws_plus)', '\\s+(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_whitespace)', '\\s*(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_whitespace_plus)', '\\s+(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_whitespaces)', '\\s+(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_space)', ' *(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_space_plus)', ' +(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_just_spaces)', ' +(?P<v1>[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(var_v1, head_raw)', '(?P<v1>([a-zA-Z][a-zA-Z0-9]*)|head)'),
            ('word(var_v1, tail)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)$'),
            ('word(var_v1, tail_ws)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s*$'),
            ('word(var_v1, tail_ws_plus)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s+$'),
            ('word(var_v1, tail_whitespace)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s*$'),
            ('word(var_v1, tail_whitespace_plus)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s+$'),
            ('word(var_v1, tail_whitespaces)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s+$'),
            ('word(var_v1, tail_space)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*) *$'),
            ('word(var_v1, tail_space_plus)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*) +$'),
            ('word(var_v1, tail_spaces)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*) +$'),
            ('word(var_v1, tail_just_ws)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s*'),
            ('word(var_v1, tail_just_ws_plus)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s+'),
            ('word(var_v1, tail_just_whitespace)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s*'),
            ('word(var_v1, tail_just_whitespace_plus)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s+'),
            ('word(var_v1, tail_just_whitespaces)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*)\\s+'),
            ('word(var_v1, tail_just_space)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*) *'),
            ('word(var_v1, tail_just_space_plus)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*) +'),
            ('word(var_v1, tail_just_spaces)', '(?P<v1>[a-zA-Z][a-zA-Z0-9]*) +'),
            ('word(var_v1, tail_raw)', '(?P<v1>([a-zA-Z][a-zA-Z0-9]*)|tail)'),
            ('letter(var_word, repetition_3)', '(?P<word>[a-zA-Z]{3})'),
            ('letter(var_word, repetition_3_8)', '(?P<word>[a-zA-Z]{3,8})'),
            ('letter(var_word, repetition_3_)', '(?P<word>[a-zA-Z]{3,})'),
            ('letter(var_word, repetition__8)', '(?P<word>[a-zA-Z]{,8})'),
            ('word(var_v1, N/A, repetition_3, word_bound)', '(?P<v1>\\b((([a-zA-Z][a-zA-Z0-9]*){3})|N/A)\\b)'),
            ('letter(0_or_1_occurrence)', '[a-zA-Z]?'),
            ('letter(0_or_more_occurrence)', '[a-zA-Z]*'),
            ('letter(1_or_more_occurrence)', '[a-zA-Z]+'),
            ('letter(3_or_more_occurrence)', '[a-zA-Z]{3,}'),
            ('letter(at_least_0_occurrence)', '[a-zA-Z]*'),
            ('letter(at_least_1_occurrence)', '[a-zA-Z]{1,}'),
            ('letter(at_least_3_occurrence)', '[a-zA-Z]{3,}'),
            ('letter(at_most_0_occurrence)', '[a-zA-Z]?'),
            ('letter(at_most_1_occurrence)', '[a-zA-Z]{,1}'),
            ('letter(at_most_3_occurrence)', '[a-zA-Z]{,3}'),
            ('letter(0_occurrence)', '[a-zA-Z]?'),
            ('letter(1_occurrence)', '[a-zA-Z]'),
            ('letter(3_occurrence)', '[a-zA-Z]{3}'),
            ('word(0_or_1_occurrence)', '([a-zA-Z][a-zA-Z0-9]*)?'),
            ('word(var_v1, 0_or_1_occurrence)', '(?P<v1>([a-zA-Z][a-zA-Z0-9]*)?)'),
            ('word(var_v1, 0_or_1_occurrence, N/A)', '(?P<v1>(([a-zA-Z][a-zA-Z0-9]*)?)|N/A)'),

            ('word(0_or_1_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)?'),
            ('word(0_or_more_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*'),
            ('word(1_or_more_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)+'),
            ('word(3_or_more_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*){3,}'),
            ('word(at_least_0_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*'),
            ('word(at_least_1_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*){1,}'),
            ('word(at_least_3_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*){3,}'),
            ('word(at_most_0_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)?'),
            ('word(at_most_1_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*){,1}'),
            ('word(at_most_3_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*){,3}'),
            ('word(0_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)?'),
            ('word(1_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)'),
            ('word(3_phrase_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*){3}'),

            ('word(0_or_1_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)?'),
            ('word(0_or_more_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)*'),
            ('word(1_or_more_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)+'),
            ('word(3_or_more_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){3,}'),
            ('word(at_least_0_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)*'),
            ('word(at_least_1_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){1,}'),
            ('word(at_least_3_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){3,}'),
            ('word(at_most_0_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)?'),
            ('word(at_most_1_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){,1}'),
            ('word(at_most_3_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){,3}'),
            ('word(0_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)?'),
            ('word(1_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*)'),
            ('word(3_group_occurrence)', '[a-zA-Z][a-zA-Z0-9]*( +[a-zA-Z][a-zA-Z0-9]*){3}'),
        ]
    )
    def test_element_pattern_combining_other_flag(self, data, expected_result):
        pattern = ElementPattern(data)
        assert pattern == expected_result
        try:
            re.compile(pattern)
        except Exception as ex:
            error = 'invalid pattern: %r (err-msg: %s)' % (pattern, ex)
            assert False, error
