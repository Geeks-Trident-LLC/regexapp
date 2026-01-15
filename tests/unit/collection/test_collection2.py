import pytest       # noqa
import re

from regexapp import LinePattern


class TestLinePattern:
    @pytest.mark.parametrize(
        (
            'test_data', 'user_prepared_data', 'expected_pattern',
            'prepended_ws', 'appended_ws', 'ignore_case',
            'is_matched'
        ),
        [
            (
                ' \t\v',      # test data
                ' ',                # user prepared data
                '^\\s*$',           # expected pattern
                False, False, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',  # noqa
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',    # noqa
                '[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]* is (up|down|(administratively down)), line protocol is (up|down|(administratively down))',   # noqa
                False, False, False,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',  # noqa
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',    # noqa
                '[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]* is (up|down|(administratively down)), line protocol is (up|down|(administratively down))',     # noqa
                False, False, False,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',      # noqa
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',    # noqa
                '(?i)[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]* is (up|down|(administratively down)), line protocol is (up|down|(administratively down))',     # noqa
                False, False, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',      # noqa
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',    # noqa
                '(?i)^\\s*[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]* is (up|down|(administratively down)), line protocol is (up|down|(administratively down))',    # noqa
                True, False, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',      # noqa
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',    # noqa
                '(?i)^\\s*[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]* is (up|down|(administratively down)), line protocol is (up|down|(administratively down))\\s*$',   # noqa
                True, True, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',      # noqa
                'mixed_word(var_interface_name) is choice(up, down, administratively down, var_interface_status), line protocol is choice(up, down, administratively down, var_protocol_status)',   # noqa
                '(?i)^\\s*(?P<interface_name>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*) is (?P<interface_status>up|down|(administratively down)), line protocol is (?P<protocol_status>up|down|(administratively down))\\s*$',    # noqa
                True, True, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',      # noqa
                'mixed_word(var_interface_name) is words(var_interface_status), line protocol is words(var_protocol_status)',   # noqa
                '(?i)(?P<interface_name>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*) is (?P<interface_status>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*), line protocol is (?P<protocol_status>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)',    # noqa
                False, False, True,
                True
            ),
            (
                '   Lease Expires . . . . . . . . . . : Sunday, April 11, 2021 8:43:33 AM',  # test data
                '   Lease Expires . . . . . . . . . . : datetime(var_datetime, format3)',    # user prepared data
                '(?i) +Lease Expires (\\. ){2,}: (?P<datetime>[a-zA-Z]{6,9}, [a-zA-Z]{3,9} +\\d{1,2}, \\d{4} 1?\\d:\\d{2}:\\d{2} [apAP][mM])',  # noqa
                False, False, True,
                True
            ),
            (
                'vagrant  + pts/0        2021-04-11 02:58   .          1753 (10.0.2.2)',                    # test data
                'vagrant  + pts/0        datetime(var_datetime, format4)   .          1753 (10.0.2.2)',     # noqa
                '(?i)vagrant +\\+ pts/0 +(?P<datetime>\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}) +\\. +1753 \\(10\\.0\\.2\\.2\\)',  # noqa
                False, False, True,
                True
            ),
            (
                '   Lease Expires . . . . . . . . . . : Sunday, April 11, 2021 8:43:33 AM',         # test data
                '   Lease Expires . . . . . . . . . . : datetime(var_datetime, format3, format4)',  # user prepared data
                '(?i) +Lease Expires (\\. ){2,}: (?P<datetime>([a-zA-Z]{6,9}, [a-zA-Z]{3,9} +\\d{1,2}, \\d{4} 1?\\d:\\d{2}:\\d{2} [apAP][mM])|(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}))',     # noqa
                False, False, True,
                True
            ),
            (
                'vagrant  + pts/0        2021-04-11 02:58   .          1753 (10.0.2.2)',                            # noqa
                'vagrant  + pts/0        datetime(var_datetime, format3, format4)   .          1753 (10.0.2.2)',    # noqa
                '(?i)vagrant +\\+ pts/0 +(?P<datetime>([a-zA-Z]{6,9}, [a-zA-Z]{3,9} +\\d{1,2}, \\d{4} 1?\\d:\\d{2}:\\d{2} [apAP][mM])|(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2})) +\\. +1753 \\(10\\.0\\.2\\.2\\)',     # noqa
                False, False, True,
                True
            ),
            (
                '  Hardware is TenGigE, address is 0800.4539.d909 (bia 0800.4539.d909)',    # test data
                '  Hardware is TenGigE, address is mac_address() (bia mac_address())',          # user prepared data
                '(?i) +Hardware is TenGigE, address is ([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2}) \\(bia ([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})\\)',     # noqa
                False, False, True,
                True
            ),
            (
                '  Hardware is TenGigE, address is 0800.4539.d909 (bia 0800.4539.d909)',  # test data
                '  Hardware is TenGigE, address is mac_address(var_addr1) (bia mac_address(var_addr2))',  # noqa
                '(?i) +Hardware is TenGigE, address is (?P<addr1>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})) \\(bia (?P<addr2>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2}))\\)',    # noqa
                False, False, True,
                True
            ),
            (
                'addresses are 11-22-33-44-55-aa, 11:22:33:44:55:bb, 11 22 33 44 55 cc, 1122.3344.55dd',    # test data
                'addresses are mac_address(var_addr1), mac_address(var_addr2), mac_address(var_addr3), mac_address(var_addr4)',     # noqa
                '(?i)addresses are (?P<addr1>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})), (?P<addr2>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})), (?P<addr3>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})), (?P<addr4>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2}))',  # noqa
                False, False, True,
                True
            ),
            (
                'today is Friday.',                         # test data
                'today is word(var_day, word_bound).',      # user prepared data
                '(?i)today is (?P<day>\\b[a-zA-Z][a-zA-Z0-9]*\\b)\\.',    # expected pattern
                False, False, True,
                True
            ),
            (
                'cherry is delicious.',                     # test data
                'word(var_fruit, head) is delicious.',      # user prepared data
                '(?i)^(?P<fruit>[a-zA-Z][a-zA-Z0-9]*) is delicious\\.',     # expected pattern
                False, False, True,
                True
            ),
            (
                'cherry is delicious.',                             # test data
                'word(var_fruit, head_ws) is delicious.',        # user prepared data
                '(?i)^\\s*(?P<fruit>[a-zA-Z][a-zA-Z0-9]*) is delicious\\.',     # expected pattern
                False, False, True,
                True
            ),
            (
                '\r\n cherry is delicious.',                        # test data
                'word(var_fruit, head_ws) is delicious.',        # user prepared data
                '(?i)^\\s*(?P<fruit>[a-zA-Z][a-zA-Z0-9]*) is delicious\\.',     # expected pattern
                False, False, True,
                True
            ),
            (
                'I live in ABC',                                        # test data
                'I live in words(var_city, tail)',                     # user prepared data
                '(?i)I live in (?P<city>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)$',        # expected pattern
                False, False, True,
                True
            ),
            (
                'I live in ABC',                                        # test data
                'I live in words(var_city, tail_ws)',                  # user prepared data
                '(?i)I live in (?P<city>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)\\s*$',    # expected pattern
                False, False, True,
                True
            ),
            (
                'I live in ABC \r\n',                                   # test data
                'I live in words(var_city, tail_ws)',                  # user prepared data
                '(?i)I live in (?P<city>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)\\s*$',    # expected pattern
                False, False, True,
                True
            ),
            (
                '          inet addr:10.0.2.15  Bcast:10.0.2.255  Mask:255.255.255.0',  # test data
                '          inet addr:ipv4_address(var_inet_addr)  Bcast:ipv4_address(var_bcast_addr)  Mask:ipv4_address(var_mask_addr)',  # noqa
                '(?i) +inet addr:(?P<inet_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3}) +Bcast:(?P<bcast_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3}) +Mask:(?P<mask_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3})',  # noqa
                False, False, True,
                True
            ),
            (
                '192.168.0.1 is IPv4 address',  # test data
                'ipv4_address() is IPv4 address',  # user prepared data
                '(?i)((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3} is IPv4 address',  # noqa
                False, False, True,
                True
            ),
            (
                'Is 192.168.0.256 an IPv4 address?',  # test data
                'Is ipv4_address() an IPv4 address?',  # user prepared data
                '(?i)Is ((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3} an IPv4 address\\?',     # noqa
                False, False, True,
                False
            ),
            (
                '1::a is IPv6 address',  # test data
                'ipv6_address(var_addr) is IPv6 address',  # user prepared data
                '(?i)(?P<addr>([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4})) is IPv6 address',    # noqa
                False, False, True,
                True
            ),
            (
                'Is 1:::a an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is (?P<addr>([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4})) an IPv6 address',    # noqa
                False, False, True,
                False
            ),
            (
                'Is 1:2:3:4:55555:a an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is (?P<addr>([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4})) an IPv6 address',    # noqa
                False, False, True,
                False
            ),
            (
                'Is 1:2:3:4:5:abgd an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is (?P<addr>([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4})) an IPv6 address',    # noqa
                False, False, True,
                False
            ),
            (
                'Is 1::3:4::a an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is (?P<addr>([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4})) an IPv6 address',    # noqa
                False, False, True,
                False
            ),
            (
                'cherry is delicious.',  # test data
                'start()cherry is delicious.',  # user prepared data
                '(?i)^cherry is delicious\\.',  # expected pattern
                False, False, True,
                True
            ),
            (
                'cherry is delicious.',  # test data
                'start() cherry is delicious.',  # user prepared data
                '(?i)^cherry is delicious\\.',  # expected pattern
                False, False, True,
                True
            ),
            (
                'cherry is delicious.',  # test data
                'start(space)word(var_fruit) is delicious.',  # user prepared data
                '(?i)^ *(?P<fruit>[a-zA-Z][a-zA-Z0-9]*) is delicious\\.',  # expected pattern
                False, False, True,
                True
            ),
            (
                'cherry is delicious.',  # test data
                'start(space) word(var_fruit) is delicious.',  # user prepared data
                '(?i)^ *(?P<fruit>[a-zA-Z][a-zA-Z0-9]*) is delicious\\.',  # expected pattern
                False, False, True,
                True
            ),
            (
                'this box is green',  # test data
                'this box is green end()',  # user prepared data
                '(?i)this box is green$',  # expected pattern
                False, False, True,
                True
            ),
            (
                'this box is green',  # test data
                'this box is word(var_color)end()',  # user prepared data
                '(?i)this box is (?P<color>[a-zA-Z][a-zA-Z0-9]*)$',  # expected pattern
                False, False, True,
                True
            ),
            (
                'this box is green',  # test data
                'this box is word(var_color) end()',  # user prepared data
                '(?i)this box is (?P<color>[a-zA-Z][a-zA-Z0-9]*)$',  # expected pattern
                False, False, True,
                True
            ),
            (
                'file1.txt',  # test data
                'mixed_words(var_file_name) data(->, or_empty) mixed_words(var_link_name, or_empty) end()',
                '(?i)(?P<file_name>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)*)\\s*(->|)\\s*(?P<link_name>(([\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)*))|)$',  # noqa
                False, False, True,
                True
            ),
            (
                "'My Documents' -> /c/Users/test/Documents/",  # test data
                'mixed_words(var_file_name) data(->, or_empty) mixed_words(var_link_name, or_empty) end()',
                '(?i)(?P<file_name>[\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)*)\\s*(->|)\\s*(?P<link_name>(([\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*( [\\x21-\\x7e]*[a-zA-Z0-9][\\x21-\\x7e]*)*))|)$',    # noqa
                False, False, True,
                True
            ),
            (
                "software version is 1.1.1.",  # test data
                'software version is version(var_ver).',
                '(?i)software version is (?P<ver>[0-9]\\S*)\\.',
                # noqa
                False, False, True,
                True
            ),
        ]
    )
    def test_line_pattern(self, test_data, user_prepared_data, expected_pattern,
                          prepended_ws, appended_ws, ignore_case,
                          is_matched):
        pattern = LinePattern(
            user_prepared_data,
            prepended_ws=prepended_ws, appended_ws=appended_ws,
            ignore_case=ignore_case
        )
        assert pattern == expected_pattern
        match = re.search(pattern, test_data)
        if is_matched:
            assert match is not None
        else:
            assert match is None

    @pytest.mark.parametrize(
        (
            'test_data', 'user_prepared_data', 'expected_pattern', 'expected_statement',
            'prepended_ws', 'appended_ws', 'ignore_case'
        ),
        [
            (
                ['cherry is good for health'],  # test data
                'cherry is good for health',    # user prepared data
                '^\\s*cherry is good for health',  # expected pattern
                '^\\s*cherry is good for health',  # expected statement
                True, False, False,
            ),
            (
                ['cherry is good for health'],  # test data
                'word() is words()',  # user prepared data
                '^\\s*[a-zA-Z][a-zA-Z0-9]* is [a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*',  # expected pattern
                '^\\s*[a-zA-Z][a-zA-Z0-9]* is [a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*',  # expected statement
                True, False, False,
            ),
            (
                ['cherry is good for health'],  # test data
                'word(var_fruit) is words(var_desc)',  # user prepared data
                '^\\s*(?P<fruit>[a-zA-Z][a-zA-Z0-9]*) is (?P<desc>[a-zA-Z][a-zA-Z0-9]*( [a-zA-Z][a-zA-Z0-9]*)*)',  # expected pattern
                '^\\s*${fruit} is ${desc}',     # expected statement
                True, False, False,
            ),
            (
                ['123   abc   567'],    # test data
                'digits(var_v1)   letters(var_v2)     digits(var_v3)',  # user prepared data
                '^\\s*(?P<v1>\\d+) +(?P<v2>[a-zA-Z]+) +(?P<v3>\\d+)',  # expected pattern
                '^\\s*${v1} +${v2} +${v3}',  # expected statement
                True, False, False,
            ),
            (
                [
                    '123   abc   567',
                    '123   567'
                ],  # test data
                'digits(var_v1)   letters(var_v2, or_empty)     digits(var_v3)',  # user prepared data
                '^\\s*(?P<v1>\\d+)\\s*(?P<v2>([a-zA-Z]+)|) +(?P<v3>\\d+)',  # expected pattern
                '^\\s*${v1}\\s*${v2} +${v3}',  # expected statement
                True, False, False,
            ),
            (
                [
                    '123   abc   567',
                    '123   567'
                ],  # test data
                'digits(var_v1)   letters(var_v2, or_empty)   digits(var_v3)',  # user prepared data
                '^\\s*(?P<v1>\\d+)\\s*(?P<v2>([a-zA-Z]+)|) +(?P<v3>\\d+)',  # expected pattern
                '^\\s*${v1}\\s*${v2} +${v3}',  # expected statement
                True, False, False,
            ),
            (
                [
                    '123   abc   567',
                    '123   abc'
                ],  # test data
                'digits(var_v1)   letters(var_v2)     digits(var_v3, or_empty)',  # user prepared data
                '^\\s*(?P<v1>\\d+) +(?P<v2>[a-zA-Z]+)\\s*(?P<v3>(\\d+)|)',  # expected pattern
                '^\\s*${v1} +${v2}\\s*${v3}',  # expected statement
                True, False, False,
            ),
            (
                [
                    '123   abc   567',
                    '124   abd',
                    '125'
                ],  # test data
                'digits(var_v1)   letters(var_v2, or_empty)     digits(var_v3, or_empty)',  # user prepared data
                '^\\s*(?P<v1>\\d+)\\s*(?P<v2>([a-zA-Z]+)|)\\s*(?P<v3>(\\d+)|)',  # expected pattern
                '^\\s*${v1}\\s*${v2}\\s*${v3}',  # expected statement
                True, False, False,
            ),
            (
                [
                    '123   abc   567  ',
                    '124   abd        ',
                    '125              '
                ],  # test data
                'digits(var_v1)   letters(var_v2, or_empty)     digits(var_v3, or_empty)  ',  # user prepared data
                '^\\s*(?P<v1>\\d+)\\s*(?P<v2>([a-zA-Z]+)|)\\s*(?P<v3>(\\d+)|)\\s*',  # expected pattern
                '^\\s*${v1}\\s*${v2}\\s*${v3}\\s*',  # expected statement
                True, False, False,
            ),
        ]
    )
    def test_line_statement(self, test_data, user_prepared_data,
                            expected_pattern, expected_statement,
                            prepended_ws, appended_ws, ignore_case):
        pattern = LinePattern(user_prepared_data,
                              prepended_ws=prepended_ws,
                              appended_ws=appended_ws, ignore_case=ignore_case)
        assert pattern == expected_pattern
        assert pattern.statement == expected_statement

        for line in test_data:
            match = re.search(pattern, line)    # noqa
            assert match is not None
