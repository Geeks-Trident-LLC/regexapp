import pytest       # noqa
import re
from regexapp import ElementPattern


class TestElementPatternD:

    @pytest.mark.parametrize(
        ('data', 'expected_result'),
        [
            ####################################################################
            # predefined keyword test                                          #
            ####################################################################
            ('datetime()', '\\d{2}/\\d{2}/\\d{4} \\d{2}:\\d{2}:\\d{2}'),
            ('datetime(format)', '\\d{2}/\\d{2}/\\d{4} \\d{2}:\\d{2}:\\d{2}'),
            ('datetime(format1)', '\\d{2}-\\d{2}-\\d{4} \\d{2}:\\d{2}:\\d{2}'),
            ('datetime(format1, format3)', '((\\d{2}-\\d{2}-\\d{4} \\d{2}:\\d{2}:\\d{2})|([a-zA-Z]{6,9}, [a-zA-Z]{3,9} +\\d{1,2}, \\d{4} 1?\\d:\\d{2}:\\d{2} [apAP][mM]))'),      # noqa
            ('datetime(var_datetime, format1, format3)', '(?P<datetime>(\\d{2}-\\d{2}-\\d{4} \\d{2}:\\d{2}:\\d{2})|([a-zA-Z]{6,9}, [a-zA-Z]{3,9} +\\d{1,2}, \\d{4} 1?\\d:\\d{2}:\\d{2} [apAP][mM]))'),    # noqa
            ('datetime(var_datetime, format1, format3, n/a)', '(?P<datetime>(\\d{2}-\\d{2}-\\d{4} \\d{2}:\\d{2}:\\d{2})|([a-zA-Z]{6,9}, [a-zA-Z]{3,9} +\\d{1,2}, \\d{4} 1?\\d:\\d{2}:\\d{2} [apAP][mM])|n/a)'),   # noqa

        ]
    )
    def test_datetime_element_pattern(self, data, expected_result):
        pattern = ElementPattern(data)
        assert pattern == expected_result
        try:
            re.compile(pattern)
        except Exception as ex:
            error = 'invalid pattern: %r (err-msg: %s)' % (pattern, ex)
            assert False, error
