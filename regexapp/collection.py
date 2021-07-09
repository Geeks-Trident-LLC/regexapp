import re
import yaml
from pathlib import Path, PurePath

import logging
logger = logging.getLogger(__file__)


def validate_pattern(pattern, flags=0, exception_cls=None):
    """validate a pattern

    Parameters
    ----------
    pattern (str): a pattern.
    exception_cls (Exception): an exception class.  Default is None.
    """
    exception_cls = exception_cls or Exception
    try:
        re.compile(pattern, flags=flags)
    except Exception as ex:
        msg = '{} - {}'.format(type(ex).__name__, ex)
        raise exception_cls(msg)


class PatternReferenceError(Exception):
    """Use to capture error for PatternReference instance"""


class PatternReference(dict):
    """Use to load regular expression pattern from system_settings.yaml
    or/and user_settings.yaml

    Attribute
    ---------
    sys_ref_loc (str): a system settings file name.
    user_ref_loc (str): a user settings file name.

    Methods
    -------
    load_reference(filename) -> None

    Raises
    ------
    PatternReferenceError: raise exception if filename doesn't exist or
            an invalid format
    """

    # regexp pattern - from system settings
    sys_ref_loc = str(PurePath(Path(__file__).parent, 'system_settings.yaml'))
    # regex patterns - from user settings
    user_ref_loc = str(PurePath(Path.home(), '.regexapp', 'user_settings.yaml'))

    def __init__(self):
        self.load_reference(self.sys_ref_loc)
        self.load_reference(self.user_ref_loc)

    def load_reference(self, filename):
        """Load reference from YAML settings file.
        Parameters
        ----------
        filename (str): a file name.

        Returns
        -------
        None: no return

        Raises
        ------
        PatternReferenceError: raise exception if filename doesn't exist or
                an invalid format
        """
        node = Path(filename)
        if not node.exists():
            if filename == self.sys_ref_loc:
                msg = '{} is NOT FOUND.'.format(filename)
                raise PatternReferenceError(msg)
            else:
                fmt = '%s is NOT existed.  CANT load reference.'
                logger.warning(fmt, filename)
                return

        try:
            with node.open() as stream:
                yaml_obj = yaml.load(stream, Loader=yaml.SafeLoader)

                if not yaml_obj:
                    return

                if not isinstance(yaml_obj, dict):
                    fmt = '{} must be structure as dictionary.'
                    raise PatternReferenceError(fmt.format(filename))

                for key, value in yaml_obj.items():
                    if key not in self:
                        self[key] = value
                    else:
                        fmt = ('%r key is already existed.  '
                               'Wont update %r data to key.')
                        logger.warning(fmt, key, value)
        except Exception as ex:
            msg = '{} - {}'.format(type(ex).__name__, ex)
            raise PatternReferenceError(msg)

REF = PatternReference()


class PatternError(Exception):
    """Use to capture error during pattern conversion."""


class TextPattern(str):
    """Use to convert text data to regex pattern

    Parameters
    ----------
    data (str): a text.
    used_space (bool): use space character instead of whitespace regex.
            Default is True.

    Methods
    -------
    TextPattern.get_pattern(text, used_space=True) -> str

    Raises
    ------
    PatternError: raise an exception if pattern is invalid.

    """
    def __new__(cls, data, used_space=True):
        data = str(data)
        if data:
            text_pattern = cls.get_pattern(data, used_space=used_space)
        else:
            text_pattern = ''
        return str.__new__(cls, text_pattern)

    @classmethod
    def get_pattern(cls, text, used_space=True):
        """convert data to regex pattern

        Parameters
        ----------
        text (str): a text
        used_space (bool): use a space character instead of whitespace regex.
                Default is True.

        Returns
        -------
        str: a regex pattern.

        Raises
        ------
        PatternError: raise an exception if pattern is invalid.
        """

        pattern = ' +' if used_space else r'\s+'
        result = []
        for item in re.split(pattern, text):
            if not item:
                result.append(item)
            else:
                lst = []
                for v in list(item):
                    lst += re.escape(v) if v in '^$.?*+|{}[]()' else v
                result.append(''.join(lst))
        text_pattern = pattern.join(result)

        try:
            re.compile(text_pattern)
        except Exception as ex:
            msg = '{} - {}'.format(type(ex).__name__, ex)
            raise PatternError(msg)

        return text_pattern


class ElementPattern(str):
    """Use to convert element data to regex pattern

    Parameters
    ----------
    data (str): a text.

    Methods
    -------
    ElementPattern.get_pattern(data) -> str
    ElementPattern.build_pattern(keyword, params) -> str
    ElementPattern.build_custom_pattern(keyword, params) -> bool, str
    ElementPattern.build_choice_pattern(keyword, params) -> bool, str
    ElementPattern.build_raw_pattern(keyword, params) -> bool, str
    ElementPattern.build_default_pattern(keyword, params) -> bool, str
    ElementPattern.join_list(lst) -> str
    ElementPattern.add_var_name(pattern, name='') -> str

    Raises
    ------
    PatternError: raise an exception if pattern is invalid.

    """
    def __new__(cls, data):
        data = str(data)
        if data:
            pattern = cls.get_pattern(data)
        else:
            pattern = ''
        return str.__new__(cls, pattern)

    @classmethod
    def get_pattern(cls, text):
        """convert data to regex pattern

        Parameters
        ----------
        text (str): a text

        Returns
        -------
        str: a regex pattern.

        Raises
        ------
        PatternError: raise an exception if pattern is invalid.
        """
        sep_pat = r'(?P<keyword>\w+)[(](?P<params>.*)[)]$'
        match = re.match(sep_pat, text.strip())
        if match:
            keyword = match.group('keyword')
            params = match.group('params')
            pattern = cls.build_pattern(keyword, params)
        try:
            re.compile(pattern)
            return pattern
        except Exception as ex:
            msg = '{} - {}'.format(type(ex).__name__, ex)
            raise PatternError(msg)

    @classmethod
    def build_pattern(cls, keyword, params):
        """build a regex pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        is_built, raw_pattern = cls.build_raw_pattern(keyword, params)
        if is_built:
            return raw_pattern

        is_built, custom_pattern = cls.build_custom_pattern(keyword, params)
        if is_built:
            return custom_pattern

        is_built, choice_pattern = cls.build_choice_pattern(keyword, params)
        if is_built:
            return choice_pattern

        _, default_pattern = cls.build_default_pattern(keyword, params)
        return default_pattern

    @classmethod
    def build_custom_pattern(cls, keyword, params):
        """build a regex pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        tuple: status, a regex pattern.
        """
        if keyword not in REF:
            return False, ''

        arguments = re.split(r' *, *', params) if params else []

        lst = [REF.get(keyword).get('pattern')]

        name, vpat = '', r'var_(?P<name>\w+)$'
        or_pat = r'or_(?P<case>[^,]+)'
        is_empty = False

        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match:
                name = match.group('name') if not name else name
            else:
                match = re.match(or_pat, arg, flags=re.I)
                if match:
                    case = match.group('case')
                    if case == 'empty':
                        is_empty = True
                    else:
                        if case in REF:
                            lst.append(REF.get(case).get('pattern'))
                        else:
                            lst.append(case)
                else:
                    lst.append(re.escape(arg))

        is_empty and lst.append('')
        pattern = cls.join_list(lst)
        pattern = cls.add_var_name(pattern, name)
        pattern = pattern.replace('__comma__', ',')
        return True, pattern

    @classmethod
    def build_choice_pattern(cls, keyword, params):
        """build a regex pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        if keyword != 'choice':
            return False, ''

        arguments = re.split(r' *, *', params) if params else []
        lst = []
        name, vpat = '', r'var_(?P<name>\w+)$'
        for arg in arguments:
            match = re.match(vpat, arg, flags=re.I)
            if match:
                name = match.group('name') if not name else name
            else:
                lst.append(arg)

        pattern = cls.join_list(lst)
        pattern = cls.add_var_name(pattern, name)
        pattern = pattern.replace('__comma__', ',')
        return True, pattern

    @classmethod
    def build_raw_pattern(cls, keyword, params):
        """build a regex pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        str: a regex pattern.
        """
        if not params.startswith('raw>>>'):
            return False, ''
        params = re.sub(r'raw>+', '', params, count=1)
        pattern = re.escape('{}({})'.format(keyword, params))
        return True, pattern

    @classmethod
    def build_default_pattern(cls, keyword, params):
        """build a regex pattern over given keyword, params

        Parameters
        ----------
        keyword (str): a custom keyword
        params (str): a list of parameters

        Returns
        -------
        tuple: status, a regex pattern.
        """
        pattern = re.escape('{}({})'.format(keyword, params))
        return True, pattern

    @classmethod
    def join_list(cls, lst):
        """join item of list

        Parameters
        ----------
        lst (list): list of pattern

        Returns
        -------
        str: a string data.
        """
        new_lst = []
        if len(lst) > 1:
            for item in lst:
                v = '({})'.format(item) if re.search(r'\s', item) else item
                new_lst.append(v)
        else:
            new_lst = lst

        result = '|'.join(new_lst)
        return result

    @classmethod
    def add_var_name(cls, pattern, name=''):
        """add var name to regex pattern

        Parameters
        ----------
        pattern (str): a pattern
        name (str): a regex variable name

        Returns
        -------
        str: new pattern with variable name.
        """
        if name:
            new_pattern = '(?P<{}>{})'.format(name, pattern)
            return new_pattern
        return pattern


class LinePatternError(PatternError):
    """Use to capture error during pattern conversion."""


class LinePattern(str):
    """Use to convert a line text to regex pattern

    Parameters
    ----------
    text (str): a text.
    used_space (bool): use space character instead of whitespace regex.
            Default is True.
    prepended_ws (bool): prepend a whitespace at the beginning of a pattern.
            Default is False.
    appended_ws (bool): append a whitespace at the end of a pattern.
            Default is False.
    ignore_case (bool): prepend (?i) at the beginning of a pattern.
            Default is True.

    Methods
    -------
    LinePattern.get_pattern(text, used_space=True) -> str

    Raises
    ------
    LinePatternError: raise an exception if pattern is invalid.

    """
    def __new__(cls, text, used_space=True,
                prepended_ws=False, appended_ws=False,
                ignore_case=True):
        data = str(text)
        if data:
            pattern = cls.get_pattern(
                data, used_space=used_space, prepended_ws=prepended_ws,
                appended_ws=appended_ws, ignore_case=ignore_case
            )
        else:
            pattern = r'^\s*$'
        return str.__new__(cls, pattern)

    @classmethod
    def get_pattern(cls, text, used_space=True,
                    prepended_ws=False, appended_ws=False,
                    ignore_case=True):
        """convert text to regex pattern

        Parameters
        ----------
        text (str): a text
        used_space (bool): use space character instead of whitespace regex.
                Default is True.
        prepended_ws (bool): prepend a whitespace at the beginning of a pattern.
                Default is False.
        appended_ws (bool): append a whitespace at the end of a pattern.
                Default is False.
        ignore_case (bool): prepend (?i) at the beginning of a pattern.
                Default is True.

        Returns
        -------
        str: a regex pattern.

        Raises
        ------
        LinePatternError: raise an exception if pattern is invalid.
        """
        line = str(text)

        lst = []
        start = 0
        for m in re.finditer(r'\w+[(][^)]*[)]', line):
            pre_match = m.string[start:m.start()]
            lst.append(TextPattern(pre_match, used_space=used_space))
            lst.append(ElementPattern(m.group()))
            start = m.end()
        else:
            if start:
                after_match = m.string[start:]
                lst.append(TextPattern(after_match, used_space=used_space))

        if len(lst) == 1 and lst[0].strip() == '':
            return r'^\s*$'
        elif not lst:
            if line.strip() == '':
                return r'^\s*$'
            lst.append(TextPattern(line, used_space=used_space))

        ws_pat = r' *' if used_space else r'\s*'
        prepended_ws and lst.insert(0, '^{}'.format(ws_pat))
        ignore_case and lst.insert(0, '(?i)')
        appended_ws and lst.append('{}$'.format(ws_pat))
        pattern = ''.join(lst)
        validate_pattern(pattern, exception_cls=LinePatternError)
        return pattern