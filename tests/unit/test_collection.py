import pytest
import re
from regexapp import PatternReference
from regexapp import TextPattern
from regexapp import ElementPattern
from regexapp import LinePattern
from regexapp import PatternBuilder


class TestPatternReference:
    def test_initialization(self):
        obj = PatternReference()
        assert obj.get('word').get('pattern') == r'\w+'


class TestTextPattern:
    @pytest.mark.parametrize(
        ('data', 'used_space', 'expected_result'),
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

    def test_pattern_is_empty(self):
        text_pat = TextPattern('')
        is_empty = text_pat.is_empty
        assert is_empty

    def test_pattern_is_empty_or_whitespace(self):
        for data in ['', ' ']:
            text_pat = TextPattern(data, used_space=True)
            chk = text_pat.is_empty_or_whitespace
            assert chk

            text_pat = TextPattern(data, used_space=False)
            chk = text_pat.is_empty_or_whitespace
            assert chk

    def test_pattern_is_whitespace(self):
        data = ' '
        text_pat = TextPattern(data, used_space=True)
        chk = text_pat.is_empty_or_whitespace
        assert chk

        text_pat = TextPattern(data, used_space=False)
        chk = text_pat.is_empty_or_whitespace
        assert chk


class TestElementPattern:
    @pytest.mark.parametrize(
        ('data', 'expected_result'),
        [
            ####################################################################
            # predefined keyword test                                          #
            ####################################################################
            ('whitespace()', '\\s+'),
            ('not_whitespace()', '\\S+'),
            ('letter()', '[a-zA-Z]'),
            ('letters()', '[a-zA-Z]+'),
            ('word()', '\\w+'),
            ('words()', '\\w+( +\\w+)*'),
            ('mixed_word()', '\\S*[a-zA-Z0-9]\\S*'),
            ('mixed_words()', '\\S*[a-zA-Z0-9]\\S*( +\\S*[a-zA-Z0-9]\\S*)*'),
            ('phrase()', '\\w+( +\\w+)+'),
            ('mixed_phrase()', '\\S*[a-zA-Z0-9]\\S*( +\\S*[a-zA-Z0-9]\\S*)+'),
            ('digit()', '\\d'),
            ('digits()', '\\d+'),
            ('number()', '(\\d+)?[.]?\\d+'),
            ('signed_number()', '[+(-]?(\\d+)?[.]?\\d+[)]?'),
            ('mixed_number()', '[+\\(\\[\\$-]?(\\d+(,\\d+)*)?[.]?\\d+[\\]\\)%a-zA-Z]*'),
            ('datetime()', '[0-9]+/[0-9]+/[0-9]+'),
            ('datetime(format)', '[0-9]+/[0-9]+/[0-9]+'),
            ('datetime(format1)', '[0-9]+/[0-9]+/[0-9]+ +[0-9]+:[0-9]+:[0-9]+'),
            ('datetime(format1, format3)', '([0-9]+/[0-9]+/[0-9]+ +[0-9]+:[0-9]+:[0-9]+)|([a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+)'),
            ('datetime(var_datetime, format1, format3)', '(?P<datetime>([0-9]+/[0-9]+/[0-9]+ +[0-9]+:[0-9]+:[0-9]+)|([a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+))'),
            ('datetime(var_datetime, format1, format3, n/a)', '(?P<datetime>([0-9]+/[0-9]+/[0-9]+ +[0-9]+:[0-9]+:[0-9]+)|([a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+)|n/a)'),
            ('mac_address()', '([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})'),
            ('mac_address(or_n/a)', '([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})|n/a'),
            ('mac_address(var_mac_addr, or_n/a)', '(?P<mac_addr>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})|n/a)'),
            ('ipv4_address()', '((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3}'),
            ('ipv6_address()', '(([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4}))'),
            ####################################################################
            # predefined keyword test combining with other flags               #
            ####################################################################
            ('word(var_v1, or_empty)', '(?P<v1>\\w+|)'),
            ('word(var_v1, or_n/a, or_empty)', '(?P<v1>\\w+|n/a|)'),
            ('word(var_v1, or_abc xyz, or_12.95 19.95, or_empty)', '(?P<v1>\\w+|(abc xyz)|(12.95 19.95)|)'),
            ('word(var_v1, word_bound_left)', '(?P<v1>\\b\\w+)'),
            ('word(var_v1, word_bound_right)', '(?P<v1>\\w+\\b)'),
            ('word(var_v1, word_bound)', '(?P<v1>\\b\\w+\\b)'),
            ('word(var_v1, word_bound_raw)', '(?P<v1>\\w+|word_bound)'),
            ('word(var_v1, started)', '^(?P<v1>\\w+)'),
            ('word(var_v1, started_ws)', '^\\s*(?P<v1>\\w+)'),
            ('word(var_v1, started_ws_plus)', '^\\s+(?P<v1>\\w+)'),
            ('word(var_v1, started_space)', '^ *(?P<v1>\\w+)'),
            ('word(var_v1, started_space_plus)', '^ +(?P<v1>\\w+)'),
            ('word(var_v1, started_raw)', '(?P<v1>\\w+|started)'),
            ('word(var_v1, ended)', '(?P<v1>\\w+)$'),
            ('word(var_v1, ended_ws)', '(?P<v1>\\w+)\\s*$'),
            ('word(var_v1, ended_ws_plus)', '(?P<v1>\\w+)\\s+$'),
            ('word(var_v1, ended_space)', '(?P<v1>\\w+) *$'),
            ('word(var_v1, ended_space_plus)', '(?P<v1>\\w+) +$'),
            ('word(var_v1, ended_raw)', '(?P<v1>\\w+|ended)'),
            ('letter(var_word, repetition_3)', '(?P<word>[a-zA-Z]{3})'),
            ('letter(var_word, repetition_3_8)', '(?P<word>[a-zA-Z]{3,8})'),
            ('letter(var_word, repetition_3_)', '(?P<word>[a-zA-Z]{3,})'),
            ('letter(var_word, repetition__8)', '(?P<word>[a-zA-Z]{,8})'),
            ####################################################################
            # choice keyword test                                              #
            ####################################################################
            ('choice(up, down, administratively down)', 'up|down|(administratively down)'),
            ('choice(up, down, administratively down, var_v2)', '(?P<v2>up|down|(administratively down))'),
            ('choice(up, down, administratively down, var_v2, or_empty)', '(?P<v2>up|down|(administratively down)|)'),
            ('choice(up, down, administratively down, var_v2, or_empty, or_digits)', '(?P<v2>up|down|(administratively down)|\\d+|)'),
            ####################################################################
            # data keyword test                                                #
            ####################################################################
            ('data(->)', '->'),
            ('data(->, or_empty)', '(->|)'),
            ####################################################################
            # start keyword test                                               #
            ####################################################################
            ('start()', '^ *'),
            ('start(space)', '^ *'),
            ('start(space_plus)', '^ +'),
            ('start(ws)', '^\\s*'),
            ('start(ws_plus)', '^\\s+'),
            ####################################################################
            # end keyword test                                               #
            ####################################################################
            ('end()', '\\s*$'),
            ('end(space)', ' *$'),
            ('end(space_plus)', ' +$'),
            ('end(ws)', '\\s*$'),
            ('end(ws_plus)', '\\s+$'),
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
    def test_element_pattern(self, data, expected_result):
        pattern = ElementPattern(data)
        assert pattern == expected_result


class TestLinePattern:
    @pytest.mark.parametrize(
        (
            'test_data', 'user_prepared_data', 'expected_pattern',
            'used_space', 'prepended_ws', 'appended_ws',
            'ignore_case', 'is_matched'
        ),
        [
            (
                ' \t\n\r\f\v',      # test data
                ' ',                # user prepared data
                '^\\s*$',           # expected pattern
                True, False, False, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '\\S*[a-zA-Z0-9]\\S*\\s+is\\s+up|down|(administratively down),\\s+line\\s+protocol\\s+is\\s+up|down|(administratively down)',   # expected pattern
                False, False, False, False,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down)',               # expected pattern
                True, False, False, False,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '(?i)\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down)',           # expected pattern
                True, False, False, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '(?i)^ *\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down)',        # expected pattern
                True, True, False, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                              # test data
                'mixed_word() is choice(up, down, administratively down), line protocol is choice(up, down, administratively down)',            # user prepared data
                '(?i)^ *\\S*[a-zA-Z0-9]\\S* +is +up|down|(administratively down), +line +protocol +is +up|down|(administratively down) *$',     # expected pattern
                True, True, True, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                                                                                          # test data
                'mixed_word(var_interface_name) is choice(up, down, administratively down, var_interface_status), line protocol is choice(up, down, administratively down, var_protocol_status)',           # user prepared data
                '(?i)^ *(?P<interface_name>\\S*[a-zA-Z0-9]\\S*) +is +(?P<interface_status>up|down|(administratively down)), +line +protocol +is +(?P<protocol_status>up|down|(administratively down)) *$',  # expected pattern
                True, True, True, True,
                True
            ),
            (
                'TenGigE0/0/0/1 is administratively down, line protocol is administratively down',                                                                      # test data
                'mixed_word(var_interface_name) is words(var_interface_status), line protocol is words(var_protocol_status)',                                           # user prepared data
                '(?i)(?P<interface_name>\\S*[a-zA-Z0-9]\\S*) +is +(?P<interface_status>\\w+( +\\w+)*), +line +protocol +is +(?P<protocol_status>\\w+( +\\w+)*)',    # expected pattern
                True, False, False, True,
                True
            ),
            (
                '   Lease Expires . . . . . . . . . . : Sunday, April 11, 2021 8:43:33 AM',  # test data
                '   Lease Expires . . . . . . . . . . : datetime(var_datetime, format3)',    # user prepared data
                '(?i) +Lease +Expires +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +: +(?P<datetime>[a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+)',   # expected pattern
                True, False, False, True,
                True
            ),
            (
                'vagrant  + pts/0        2021-04-11 02:58   .          1753 (10.0.2.2)',                    # test data
                'vagrant  + pts/0        datetime(var_datetime, format4)   .          1753 (10.0.2.2)',     # user prepared data
                '(?i)vagrant +\\+ +pts/0 +(?P<datetime>[0-9]+-[0-9]+-[0-9]+ +[0-9]+:[0-9]+) +\\. +1753 +\\(10\\.0\\.2\\.2\\)',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                '   Lease Expires . . . . . . . . . . : Sunday, April 11, 2021 8:43:33 AM',         # test data
                '   Lease Expires . . . . . . . . . . : datetime(var_datetime, format3, format4)',  # user prepared data
                '(?i) +Lease +Expires +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +\\. +: +(?P<datetime>([a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+)|([0-9]+-[0-9]+-[0-9]+ +[0-9]+:[0-9]+))',     # expected pattern
                True, False, False, True,
                True
            ),
            (
                'vagrant  + pts/0        2021-04-11 02:58   .          1753 (10.0.2.2)',                            # test data
                'vagrant  + pts/0        datetime(var_datetime, format3, format4)   .          1753 (10.0.2.2)',    # user prepared data
                '(?i)vagrant +\\+ +pts/0 +(?P<datetime>([a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+)|([0-9]+-[0-9]+-[0-9]+ +[0-9]+:[0-9]+)) +\\. +1753 +\\(10\\.0\\.2\\.2\\)',     # expected pattern
                True, False, False, True,
                True
            ),
            (
                '  Hardware is TenGigE, address is 0800.4539.d909 (bia 0800.4539.d909)',    # test data
                '  Hardware is TenGigE, address is mac_address() (mac_address())',          # user prepared data
                '(?i) +Hardware +is +TenGigE, +address +is +([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2}) +\\(([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})\\)',     # expected pattern
                True, False, False, True,
                True
            ),
            (
                '  Hardware is TenGigE, address is 0800.4539.d909 (bia 0800.4539.d909)',  # test data
                '  Hardware is TenGigE, address is mac_address(var_addr1) (bia mac_address(var_addr2))',  # user prepared data
                '(?i) +Hardware +is +TenGigE, +address +is +(?P<addr1>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})) +\\(bia +(?P<addr2>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2}))\\)',    # expected pattern
                True, False, False, True,
                True
            ),
            (
                'addresses are 11-22-33-44-55-aa, 11:22:33:44:55:bb, 11 22 33 44 55 cc, 1122.3344.55dd',    # test data
                'addresses are mac_address(var_addr1), mac_address(var_addr2), mac_address(var_addr3), mac_address(var_addr4)',     # user prepared data
                '(?i)addresses +are +(?P<addr1>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})), +(?P<addr2>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})), +(?P<addr3>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2})), +(?P<addr4>([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})|([0-9a-fA-F]{2}( [0-9a-fA-F]{2}){5})|([0-9a-fA-F]{4}([.][0-9a-fA-F]{4}){2}))',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'today is Friday.',                         # test data
                'today is word(var_day, word_bound).',      # user prepared data
                '(?i)today +is +(?P<day>\\b\\w+\\b)\\.',    # expected pattern
                True, False, False, True,
                True
            ),
            (
                'cherry is delicious.',                     # test data
                'word(var_fruit, started) is delicious.',   # user prepared data
                '(?i)^(?P<fruit>\\w+) +is +delicious\\.', # expected pattern
                True, False, False, True,
                True
            ),
            (
                'cherry is delicious.',                             # test data
                'word(var_fruit, started_ws) is delicious.',        # user prepared data
                '(?i)^\\s*(?P<fruit>\\w+) +is +delicious\\.',     # expected pattern
                True, False, False, True,
                True
            ),
            (
                '\r\n cherry is delicious.',                        # test data
                'word(var_fruit, started_ws) is delicious.',        # user prepared data
                '(?i)^\\s*(?P<fruit>\\w+) +is +delicious\\.',     # expected pattern
                True, False, False, True,
                True
            ),
            (
                'I live in ABC',                                        # test data
                'I live in words(var_city, ended)',                     # user prepared data
                '(?i)I +live +in +(?P<city>\\w+( +\\w+)*)$',        # expected pattern
                True, False, False, True,
                True
            ),
            (
                'I live in ABC',                                        # test data
                'I live in words(var_city, ended_ws)',                  # user prepared data
                '(?i)I +live +in +(?P<city>\\w+( +\\w+)*)\\s*$',    # expected pattern
                True, False, False, True,
                True
            ),
            (
                'I live in ABC \r\n',                                   # test data
                'I live in words(var_city, ended_ws)',                  # user prepared data
                '(?i)I +live +in +(?P<city>\\w+( +\\w+)*)\\s*$',    # expected pattern
                True, False, False, True,
                True
            ),
            (
                '          inet addr:10.0.2.15  Bcast:10.0.2.255  Mask:255.255.255.0',  # test data
                '          inet addr:ipv4_address(var_inet_addr)  Bcast:ipv4_address(var_bcast_addr)  Mask:ipv4_address(var_mask_addr)',  # user prepared data
                '(?i) +inet +addr:(?P<inet_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3}) +Bcast:(?P<bcast_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3}) +Mask:(?P<mask_addr>((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3})',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                '192.168.0.1 is IPv4 address',  # test data
                'ipv4_address() is IPv4 address',  # user prepared data
                '(?i)((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3} +is +IPv4 +address',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'Is 192.168.0.256 an IPv4 address?',  # test data
                'Is ipv4_address() an IPv4 address?',  # user prepared data
                '(?i)Is +((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))(\\.((25[0-5])|(2[0-4]\\d)|(1\\d\\d)|([1-9]?\\d))){3} +an +IPv4 +address\\?',
                # expected pattern
                True, False, False, True,
                False
            ),
            (
                '1::a is IPv6 address',  # test data
                'ipv6_address(var_addr) is IPv6 address',  # user prepared data
                '(?i)(?P<addr>(([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4}))) +is +IPv6 +address',    # expected pattern
                True, False, False, True,
                True
            ),
            (
                'Is 1:::a an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is +(?P<addr>(([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4}))) +an +IPv6 +address',    # expected pattern
                True, False, False, True,
                False
            ),
            (
                'Is 1:2:3:4:55555:a an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is +(?P<addr>(([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4}))) +an +IPv6 +address',    # expected pattern
                True, False, False, True,
                False
            ),
            (
                'Is 1:2:3:4:5:abgd an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is +(?P<addr>(([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4}))) +an +IPv6 +address',    # expected pattern
                True, False, False, True,
                False
            ),
            (
                'Is 1::3:4::a an IPv6 address',  # test data
                'Is ipv6_address(var_addr) an IPv6 address',  # user prepared data
                '(?i)Is +(?P<addr>(([a-fA-F0-9]{1,4}(:[a-fA-F0-9]{1,4}){5})|([a-fA-F0-9]{1,4}:(:[a-fA-F0-9]{1,4}){1,4})|(([a-fA-F0-9]{1,4}:){1,2}(:[a-fA-F0-9]{1,4}){1,3})|(([a-fA-F0-9]{1,4}:){1,3}(:[a-fA-F0-9]{1,4}){1,2})|(([a-fA-F0-9]{1,4}:){1,4}:[a-fA-F0-9]{1,4})|(([a-fA-F0-9]{1,4}:){1,4}:)|(:(:[a-fA-F0-9]{1,4}){1,4}))) +an +IPv6 +address',    # expected pattern
                True, False, False, True,
                False
            ),
            (
                'cherry is delicious.',  # test data
                'start()cherry is delicious.',  # user prepared data
                '(?i)^ *cherry +is +delicious\\.',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'cherry is delicious.',  # test data
                'start() cherry is delicious.',  # user prepared data
                '(?i)^ *cherry +is +delicious\\.',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'cherry is delicious.',  # test data
                'start(space)word(var_fruit) is delicious.',  # user prepared data
                '(?i)^ *(?P<fruit>\\w+) +is +delicious\\.',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'cherry is delicious.',  # test data
                'start(space) word(var_fruit) is delicious.',  # user prepared data
                '(?i)^ *(?P<fruit>\\w+) +is +delicious\\.',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'this box is green',  # test data
                'this box is green end()',  # user prepared data
                '(?i)this +box +is +green\\s*$',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'this box is green',  # test data
                'this box is word(var_color)end()',  # user prepared data
                '(?i)this +box +is +(?P<color>\\w+)\\s*$',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'this box is green',  # test data
                'this box is word(var_color) end()',  # user prepared data
                '(?i)this +box +is +(?P<color>\\w+)\\s*$',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                'file1.txt',  # test data
                'mixed_words(var_file_name) data(->, or_empty) mixed_words(var_link_name, or_empty) end()',  # user prepared data
                '(?i)(?P<file_name>\\S*[a-zA-Z0-9]\\S*( +\\S*[a-zA-Z0-9]\\S*)*) *(->|) *(?P<link_name>(\\S*[a-zA-Z0-9]\\S*( +\\S*[a-zA-Z0-9]\\S*)*)|)\\s*$',  # expected pattern
                True, False, False, True,
                True
            ),
            (
                "'My Documents' -> /c/Users/test/Documents/",  # test data
                'mixed_words(var_file_name) data(->, or_empty) mixed_words(var_link_name, or_empty) end()',     # user prepared data
                '(?i)(?P<file_name>\\S*[a-zA-Z0-9]\\S*( +\\S*[a-zA-Z0-9]\\S*)*) *(->|) *(?P<link_name>(\\S*[a-zA-Z0-9]\\S*( +\\S*[a-zA-Z0-9]\\S*)*)|)\\s*$',    # expected pattern
                True, False, False, True,
                True
            ),
        ]
    )
    def test_line_pattern(self, test_data, user_prepared_data,expected_pattern,
                          used_space, prepended_ws, appended_ws, ignore_case,
                          is_matched):
        pattern = LinePattern(
            user_prepared_data, used_space=used_space,
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
            'test_data', 'user_prepared_data', 'expected_pattern',
            'expected_statement', 'used_space', 'prepended_ws',
            'appended_ws', 'ignore_case'
        ),
        [
            (
                ['cherry is good for health'],  # test data
                'cherry is good for health',    # user prepared data
                '^ *cherry +is +good +for +health',  # expected pattern
                '^ *cherry +is +good +for +health',  # expected statement
                True, True, False, False,
            ),
            (
                ['cherry is good for health'],  # test data
                'word() is words()',  # user prepared data
                '^ *\\w+ +is +\\w+( +\\w+)*',  # expected pattern
                '^ *\\w+ +is +\\w+( +\\w+)*',  # expected statement
                True, True, False, False,
            ),
            (
                ['cherry is good for health'],  # test data
                'word(var_fruit) is words(var_desc)',  # user prepared data
                '^ *(?P<fruit>\\w+) +is +(?P<desc>\\w+( +\\w+)*)',  # expected pattern
                '^ *${fruit} +is +${desc}',     # expected statement
                True, True, False, False,
            ),
            (
                ['123   abc   567'],    # test data
                'digits(var_v1)   letters(var_v2)     digits(var_v3)',  # user prepared data
                '^ *(?P<v1>\\d+) +(?P<v2>[a-zA-Z]+) +(?P<v3>\\d+)',  # expected pattern
                '^ *${v1} +${v2} +${v3}',  # expected statement
                True, True, False, False,
            ),
            (
                [
                    '123   abc   567',
                    '123   567'
                ],  # test data
                'digits(var_v1)   letters(var_v2, or_empty)     digits(var_v3)',  # user prepared data
                '^ *(?P<v1>\\d+) *(?P<v2>[a-zA-Z]+|) +(?P<v3>\\d+)',  # expected pattern
                '^ *${v1} *${v2} +${v3}',  # expected statement
                True, True, False, False,
            ),
            (
                [
                    '123 abc 567',
                    '123 567'
                ],  # test data
                'digits(var_v1) letters(var_v2, or_empty) digits(var_v3)',  # user prepared data
                '^ *(?P<v1>\\d+) *(?P<v2>[a-zA-Z]+|) +(?P<v3>\\d+)',  # expected pattern
                '^ *${v1} *${v2} +${v3}',  # expected statement
                True, True, False, False,
            ),
            (
                [
                    '123   abc   567',
                    '123   abc'
                ],  # test data
                'digits(var_v1)   letters(var_v2)     digits(var_v3, or_empty)',  # user prepared data
                '^ *(?P<v1>\\d+) +(?P<v2>[a-zA-Z]+) *(?P<v3>\\d+|)',  # expected pattern
                '^ *${v1} +${v2} *${v3}',  # expected statement
                True, True, False, False,
            ),
        ]
    )
    def test_line_statement(self, test_data, user_prepared_data,
                            expected_pattern, expected_statement,
                            used_space,prepended_ws,appended_ws,ignore_case):
        pattern = LinePattern(user_prepared_data, used_space=used_space,
                              prepended_ws=prepended_ws,
                              appended_ws=appended_ws, ignore_case=ignore_case)
        assert pattern == expected_pattern
        assert pattern.statement == expected_statement

        for line in test_data:
            match = re.search(pattern, line)
            assert match is not None


class TestPatternBuilder:
    @pytest.mark.parametrize(
        ('test_data', 'expected_pattern', 'used_space', 'var_name'),
        [
            (
                ['Friday, April 9, 2021 8:43:15 PM'],
                '[a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+',
                True,
                ''
            ),
            (
                ['Friday, April 9, 2021 8:43:15 PM', '12/06/2010 08:56:45'],
                '([a-zA-Z]+, +[a-zA-Z]+ +[0-9]+, +[0-9]+ +[0-9]+:[0-9]+:[0-9]+ +[a-zA-Z]+)|([0-9]+/[0-9]+/[0-9]+ +[0-9]+:[0-9]+:[0-9]+)',
                True,
                ''
            ),
            (
                ['2019 Dec 16 14:44:01'],
                '[0-9]+ +[a-zA-Z]+ +[0-9]+ +[0-9]+:[0-9]+:[0-9]+',
                True,
                ''
            ),
            (
                ['2019 Dec 16 14:44:01'],
                '(?P<datetime>[0-9]+ +[a-zA-Z]+ +[0-9]+ +[0-9]+:[0-9]+:[0-9]+)',
                True,
                'datetime'
            ),
        ]
    )
    def test_pattern_builder(self, test_data, expected_pattern, used_space, var_name):
        pattern = PatternBuilder(test_data, used_space=used_space, var_name=var_name)
        assert pattern == expected_pattern
        for data in test_data:
            match = re.search(pattern, data)
            assert match is not None
