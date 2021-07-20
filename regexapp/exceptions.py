"""Module containing the exception class for regexapp."""


class PatternError(Exception):
    """Use to capture error during pattern conversion."""


class PatternReferenceError(PatternError):
    """Use to capture error for PatternReference instance"""


class TextPatternError(Exception):
    """Use to capture error during pattern conversion."""


class ElementPatternError(Exception):
    """Use to capture error during pattern conversion."""


class LinePatternError(PatternError):
    """Use to capture error during pattern conversion."""


class PatternBuilderError(PatternError):
    """Use to capture error during pattern conversion."""
