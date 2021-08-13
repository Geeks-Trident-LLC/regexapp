"""Top-level module for regexapp.

- support TextPattern, ElementPattern, LinePattern, BlockPattern, and PatternBuilder
- support predefine pattern reference on system_references.yaml
- allow end-user to customize pattern on /home/.regexapp/user_references.yaml
- allow end-user to generate on GUI application and verify it.
- dynamically generate Python unittest script
- dynamically generate Python pytest script
- dynamically generate Robotframework test script
"""

from regexapp.collection import TextPattern
from regexapp.collection import ElementPattern
from regexapp.collection import LinePattern
from regexapp.collection import PatternBuilder
from regexapp.collection import BlockPattern
from regexapp.collection import PatternReference
from regexapp.core import RegexBuilder
from regexapp.core import DynamicGenTestScript
from regexapp.core import add_reference
from regexapp.core import remove_reference

__version__ = '0.1.0'
version = __version__
__edition__ = 'Community'
edition = __edition__

__all__ = [
    'TextPattern',
    'ElementPattern',
    'LinePattern',
    'BlockPattern',
    'PatternBuilder',
    'PatternReference',
    'RegexBuilder',
    'DynamicGenTestScript',
    'add_reference',
    'remove_reference',
    'version',
    'edition',
]