import pytest       # noqa
import re
from regexapp import ElementPattern


class TestElementPatternC:
    @pytest.mark.parametrize(
        ('data', 'expected_result'),
        [
            ####################################################################
            # choice keyword test                                              #
            ####################################################################
            ('choice(up, down, administratively down)', '(up|down|(administratively down))'),
            ('choice(up, down, administratively down, var_v2)', '(?P<v2>up|down|(administratively down))'),
            ('choice(up, down, administratively down, var_v2, or_empty)', '(?P<v2>(up|down|(administratively down))|)'),
            ('choice(up, down, administratively down, var_v2, or_empty, or_digits)', '(?P<v2>(up|down|(administratively down)|(\\d+))|)'),      # noqa
            ('choice(abc, word_bound)', '\\b(abc)\\b'),
            ('choice(abc, xyz, word_bound)', '\\b(abc|xyz)\\b'),
            ('choice(var_v1, abc, xyz, word_bound)', '(?P<v1>\\b(abc|xyz)\\b)'),
            ####################################################################
            # data keyword test                                                #
            ####################################################################
            ('data(->)', '->'),
            ('data(->, or_empty)', '(->|)'),
            ####################################################################
            # symbol keyword test                                              #
            ####################################################################
            ('symbol(name=hyphen)', '-'),
            ('symbol(name=hyphen, 3_or_more_occurrence)', '-{3,}'),
            ('symbol(name=question_mark, 3_or_more_occurrence)', '\\?{3,}'),
            ('symbol(name=hexadecimal, 1_or_2_occurrence)', '[0-9a-fA-F]{1,2}'),
            ('symbol(var_v1, name=hexadecimal, 1_or_2_occurrence)', '(?P<v1>[0-9a-fA-F]{1,2})'),
            ('symbol(var_v1, name=hex, 1_or_2_occurrence, word_bound)', '(?P<v1>\\b[0-9a-fA-F]{1,2}\\b)'),
            ('symbol(var_v1, name=hex, 1_or_2_occurrence, word_bound, N/A)', '(?P<v1>\\b(([0-9a-fA-F]{1,2})|N/A)\\b)'),
            ####################################################################
            # start keyword test                                               #
            ####################################################################
            ('start()', '^'),
            ('start(space)', '^ *'),
            ('start(spaces)', '^ +'),
            ('start(space_plus)', '^ +'),
            ('start(ws)', '^\\s*'),
            ('start(ws_plus)', '^\\s+'),
            ('start(whitespace)', '^\\s*'),
            ('start(whitespaces)', '^\\s+'),
            ('start(whitespace_plus)', '^\\s+'),
            ####################################################################
            # end keyword test                                               #
            ####################################################################
            ('end()', '$'),
            ('end(space)', ' *$'),
            ('end(spaces)', ' +$'),
            ('end(space_plus)', ' +$'),
            ('end(ws)', '\\s*$'),
            ('end(ws_plus)', '\\s+$'),
            ('end(whitespace)', '\\s*$'),
            ('end(whitespaces)', '\\s+$'),
            ('end(whitespace_plus)', '\\s+$'),
            ####################################################################
            # raw data test                                                    #
            ####################################################################
            ('word(raw>>>)', 'word\\(\\)'),
            ('word(raw>>>data="")', 'word\\(data=""\\)'),
            ####################################################################
            # unknown keyword test                                             #
            ####################################################################
            ('abc_word()', 'abc_word\\(\\)'),
            ('xyz_word()', 'xyz_word\\(\\)'),
        ]
    )
    def test_element_pattern_misc(self, data, expected_result):
        pattern = ElementPattern(data)
        assert pattern == expected_result
        try:
            re.compile(pattern)
        except Exception as ex:
            error = 'invalid pattern: %r (err-msg: %s)' % (pattern, ex)
            assert False, error
