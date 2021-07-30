import re
from regexapp import LinePattern
from regexapp.exceptions import RegexBuilderError
from regexapp.exceptions import PatternReferenceError
from regexapp.collection import REF
from copy import deepcopy
from collections import OrderedDict

BASELINE_REF = deepcopy(REF)


class RegexBuilder:
    """Use for building regex pattern

    Attributes
    ----------
    user_data (str, list): a user data can be either string or list of string.
    test_data (str, list): a test data can be either string or list of string.
    used_space (bool): use space character instead of whitespace regex.
            Default is True.
    prepended_ws (bool): prepend a whitespace at the beginning of a pattern.
            Default is False.
    appended_ws (bool): append a whitespace at the end of a pattern.
            Default is False.
    ignore_case (bool): prepend (?i) at the beginning of a pattern.
            Default is False.
    line_patterns (list): a list of patterns.
    test_report (str): a test report.
    test_result (bool): a test result.
    line_pattern_table (OrderedDict): a variable holds line and pattern pair.
    pattern_line_table (OrderedDict): a variable holds pattern and line pair.

    Methods
    -------
    RegexBuilder.validate_data(data, name) -> bool
    build() -> None
    test(showed=True) -> bool

    Raises
    ------
    RegexBuilderError: if user_data or test_data is invalid format.
    """
    def __init__(self, user_data='', test_data='',
                 used_space=True, prepended_ws=False,
                 appended_ws=False, ignore_case=False):
        self.user_data = user_data
        self.test_data = test_data
        self.used_space = used_space
        self.prepended_ws = prepended_ws
        self.appended_ws = appended_ws
        self.ignore_case = ignore_case
        self.line_patterns = []
        self.test_report = ''
        self.test_result = False
        self.line_pattern_table = OrderedDict()
        self.pattern_line_table = OrderedDict()

    @classmethod
    def validate_data(cls, **kwargs):
        """validate data

        Parameters
        ----------
        kwargs (dict): keyword argument

        Returns
        -------
        bool: True or False

        Raises
        ------
        RegexBuilderError: if failed to validate data.
        """
        if not kwargs:
            msg = 'CANT validate data without providing data.'
            raise RegexBuilderError(msg)

        is_validated = True
        for name, data in kwargs.items():
            fmt = '{} MUST be string or list of string.'
            if not isinstance(data, (list, str)):
                msg = fmt.format(name)
                raise RegexBuilderError(msg)

            if isinstance(data, list):
                for line in data:
                    if not isinstance(line, str):
                        msg = fmt.format(name)
                        raise RegexBuilderError(msg)
            is_validated &= True if data else False
        return is_validated

    def build(self):
        """Build regex pattern"""
        data = self.user_data
        self.__class__.validate_data(user_data=data)

        if not data:
            self.test_report = 'CANT build regex pattern with an empty data.'
            print(self.test_report)
            return

        lines = data[:] if isinstance(data, list) else data.splitlines()

        for line in lines:
            line_pat = LinePattern(
                line, used_space=self.used_space,
                prepended_ws=self.prepended_ws,
                appended_ws=self.appended_ws,
                ignore_case=self.ignore_case
            )
            line not in self.line_patterns and self.line_patterns.append(line_pat)
            self.line_pattern_table[line] = line_pat
            self.pattern_line_table[line_pat] = line

    def test(self, showed=False):
        """test regex pattern via test data.

        Parameters
        ----------
        showed (bool): show test report if set to True.  Default is False.

        Returns
        -------
        bool: True if passed a test, otherwise, False.
        """
        data = self.test_data
        self.__class__.validate_data(test_data=data)

        if not data:
            self.test_report = 'CANT run test with an empty data.'
            showed and print(self.test_report)
            return False

        lines = data[:] if isinstance(data, list) else data.splitlines()

        result = ['Test Data:', '-' * 9, '\n'.join(lines), '']
        result += ['Matched Result:', '-' * 14]

        test_result = True
        for pat in self.line_patterns:
            is_matched = False
            lst = []
            for line in lines:
                match = re.search(pat, line)
                if match:
                    is_matched = True
                    match.groupdict() and lst.append(match.groupdict())

            test_result &= is_matched
            tr = 'NO' if not is_matched else lst if lst else 'YES'
            result.append('pattern: {}'.format(pat))
            result.append('matched: {}'.format(tr))
            result.append('-' * 10)

        self.test_result = test_result
        self.test_report = '\n'.join(result)
        showed and print(self.test_report)

        return test_result


def add_reference(name='', pattern='', **kwargs):
    """add keyword reference to PatternReference.  This is an inline adding
    PatternReference for quick test.

    Parameters
    ----------
    name (str): a keyword.
    pattern (str): a regex pattern.
    kwargs (dict): keyword argument which will use for special case such as datetime.

    Raises
    ------
    PatternReferenceError: if adding an existing keyword from
        system_settings.yaml or user_settings.yaml
    """
    if not name:
        fmt = '{} keyword can not be empty name.'
        PatternReferenceError(fmt.format(name))

    obj = dict(pattern=pattern,
               description='inline_{}_{}'.format(name, pattern))
    if name not in REF:
        REF[name] = obj
    else:
        if name == 'datetime':
            for key, value in kwargs.items():
                if re.match(r'format\d+$', key):
                    REF['datetime'][key] = value
        else:
            if name not in BASELINE_REF:
                REF[name] = obj
            else:
                fmt = ('{} already exists in system_settings.yaml '
                       'or user_settings.yaml')
                raise PatternReferenceError(fmt.format(name))

def remove_reference(name=''):
    """remove keyword reference from PatternReference.  This method only remove
    any inline adding keyword reference.

    Parameters
    ----------
    name (str): a keyword.

    Raises
    ------
    PatternReferenceError: if removing an existing keyword from
        system_settings.yaml or user_settings.yaml
    """
    if not name:
        fmt = '{} keyword can not be empty name.'
        PatternReferenceError(fmt.format(name))

    if name in REF:
        if name not in BASELINE_REF:
            REF.pop(name)
        else:
            if name == 'datetime':
                REF['datetime'] = deepcopy(BASELINE_REF['datetime'])
            else:
                fmt = ('CANT remove {!r} from system_settings.yaml '
                       'or user_settings.yaml')
                raise PatternReferenceError(fmt.format(name))
    else:
        fmt = 'CANT remove {!r} keyword because it does not exist.'
        raise PatternReferenceError(fmt.format(name))