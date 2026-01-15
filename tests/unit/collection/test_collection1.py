import pytest       # noqa
import re
from regexapp import ElementPattern


class TestElementPattern:
    @pytest.mark.parametrize(
        ('data', 'expected_result'),
        [
            ####################################################################
            # predefined keyword test                                          #
            ####################################################################
            ('anything()', '.'),
            ('something()', '.*'),
            ('everything()', '.+'),
            ('space()', ' '),
            ('spaces()', ' +'),
            ('non_space()', '[^ ]'),
            ('non_spaces()', '[^ ]+'),
            ('whitespace()', '\\s'),
            ('whitespaces()', '\\s+'),
            ('non_whitespace()', '\\S'),
            ('non_whitespaces()', '\\S+'),
            ('punctuation()', r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'),
            ('punctuations()', r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+'),
            ('non_punctuation()', r'[^\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'),
            ('non_punctuations()', r'[^\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+'),
            ('letter()', '[a-zA-Z]'),
            ('letters()', '[a-zA-Z]+'),
            ('word()', '[a-zA-Z][a-zA-Z0-9]*'),
            ('words()', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*'),
            ('mixed_word()', '[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*'),
            ('mixed_words()', '[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)*'),
            ('phrase()', '[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)+'),
            ('mixed_phrase()', '[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)+'),
            ('hexadecimal()', '[0-9a-fA-F]'),
            ('hex()', '[0-9a-fA-F]'),
            ('octal()', '[0-7]'),
            ('binary()', '[01]'),
            ('digit()', '\\d'),
            ('digits()', '\\d+'),
            ('number()', '\\d*[.]?\\d+'),
            ('signed_number()', '[+(-]?\\d*[.]?\\d+[)]?'),
            ('mixed_number()', '[+\\(\\[\\$-]?(\\d+([,:/-]\\d+)*)?[.]?\\d+[\\]\\)%a-zA-Z]*'),
            ('mac_address()', '([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})'),     # noqa
            ('mac_address(or_n/a)', '(([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})|n/a)'),     # noqa
            ('mac_address(var_mac_addr, or_n/a)', '(?P<mac_addr>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})|n/a)'),   # noqa
            ('ipv4_address()', '((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3}'),   # noqa
            ('ipv6_address()', '(([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4}))'),     # noqa
            ('interface()', '[a-zA-Z][a-zA-Z0-9_/.-]*[0-9]'),
            ('version()', '[0-9]\\S*'),
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
