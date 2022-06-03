"""Module containing the exception class for regexapp."""


class PatternError(Exception):
    """Use to capture error during pattern conversion."""


class EscapePatternError(PatternError):
    """Use to capture error during performing do_soft_regex_escape"""


class PatternReferenceError(PatternError):
    """Use to capture error for PatternReference instance"""


class TextPatternError(Exception):
    """Use to capture error during pattern conversion."""


class ElementPatternError(Exception):
    """Use to capture error during pattern conversion."""


class LinePatternError(PatternError):
    """Use to capture error during pattern conversion."""


class MultilinePatternError(PatternError):
    """Use to capture error during pattern conversion."""


class PatternBuilderError(PatternError):
    """Use to capture error during pattern conversion."""


class RegexBuilderError(Exception):
    """Use to capture error for RegexBuilder class."""
