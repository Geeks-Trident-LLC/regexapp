# import re
import yaml
from pathlib import Path, PurePath

import logging
logger = logging.getLogger(__file__)


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