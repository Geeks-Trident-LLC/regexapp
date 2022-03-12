"""Module containing the logic for the regexapp entry-points."""

import sys
import argparse
import re
import yaml
# from os import path
# from textwrap import dedent
from regexapp.application import Application
from regexapp import RegexBuilder
from regexapp.core import enclose_string


def run_gui_application(options):
    """Run regexapp GUI application.

    Parameters
    ----------
    options (argparse.Namespace): argparse.Namespace instance.

    Returns
    -------
    None: will invoke ``regexapp.Application().run()`` and ``sys.exit(0)``
    if end user requests `--gui`
    """
    if options.gui:
        app = Application()
        app.run()
        sys.exit(0)


class Cli:
    """regexapp console CLI application."""

    def __init__(self):

        parser = argparse.ArgumentParser(
            prog='regexapp',
            usage='%(prog)s [options]',
            description='%(prog)s application',
        )

        parser.add_argument(
            '--gui', action='store_true',
            help='Launch a regexapp GUI application.'
        )

        parser.add_argument(
            '-u', '--user-data', type=str, dest='user_data',
            default='',
            help='Required flag: user snippet for regex generation.'
        )

        parser.add_argument(
            '-d', '--test-data', type=str, dest='test_data',
            default='',
            help='User test data.'
        )

        parser.add_argument(
            '-t', '--test', action='store_true',
            help='To perform test between test data vs generated regex pattern.'
        )

        parser.add_argument(
            '-p', '--platform', type=str, choices=['unittest', 'pytest', 'snippet'],
            default='',
            help='A generated script choice for unittest or pytest test framework.'
        )

        parser.add_argument(
            '-s', '--setting', type=str,
            default='',
            help='Settings for generated test script.'
        )

        self.parser = parser
        self.options = self.parser.parse_args()
        self.kwargs = dict()

    def validate_cli_flags(self):
        """Validate argparse `options`.

        Returns
        -------
        bool: show ``self.parser.print_help()`` and call ``sys.exit(1)`` if
        user_data flag is empty, otherwise, return True
        """

        if not self.options.user_data:
            self.parser.print_help()
            sys.exit(1)

        pattern = r'file( *name)?:: *(?P<filename>\S*)'
        m = re.match(pattern, self.options.user_data, re.I)
        if m:
            try:
                with open(m.group('filename')) as stream:
                    self.options.user_data = stream.read()
            except Exception as ex:
                failure = '*** {}: {}'.format(type(ex).__name__, ex)
                print(failure)
                sys.exit(1)

        if self.options.test_data:
            m = re.match(pattern, self.options.test_data, re.I)
            if m:
                try:
                    with open(m.group('filename')) as stream:
                        self.options.test_data = stream.read()
                except Exception as ex:
                    failure = '*** {}: {}'.format(type(ex).__name__, ex)
                    print(failure)
                    sys.exit(1)

        if self.options.setting:
            setting = self.options.setting
            m = re.match(pattern, setting, re.I)
            if m:
                try:
                    with open(m.group('filename')) as stream:
                        content = stream.read()
                except Exception as ex:
                    failure = '*** {}: {}'.format(type(ex).__name__, ex)
                    print(failure)
                    sys.exit(1)
            else:
                other_pat = r'''(?x)(
                    prepended_ws|appended_ws|ignore_case|
                    is_line|test_name|max_words|test_cls_name|
                    author|email|company|filename): *'''
                content = re.sub(r' *: *', r': ', setting)
                content = re.sub(other_pat, r'\n\1: ', content)
                content = '\n'.join(line.strip(', ') for line in content.splitlines())

            if content:
                try:
                    kwargs = yaml.load(content, Loader=yaml.SafeLoader)
                    if isinstance(kwargs, dict):
                        self.kwargs = kwargs
                    else:
                        failure = '*** INVALID-SETTING: {}'.format(setting)
                        print(failure)
                        sys.exit(1)
                except Exception as ex:
                    failure = '*** LOADING-SETTING - {}'.format(ex)
                    print(failure)
                    sys.exit(1)

        return True

    def build_regex_pattern(self):
        """Build regex pattern"""
        factory = RegexBuilder(
            user_data=self.options.user_data,
            **self.kwargs
        )
        factory.build()
        patterns = factory.patterns
        total = len(patterns)
        if total >= 1:
            if total == 1:
                result = 'pattern = r{}'.format(enclose_string(patterns[0]))
                print(result)
            else:
                lst = []
                fmt = 'pattern{} = r{}'
                for index, pattern in enumerate(patterns, 1):
                    lst.append(fmt.format(index, enclose_string(pattern)))
                result = '\n'.join(lst)
                print(result)
            sys.exit(0)
        else:
            fmt = '*** CANT generate regex pattern from\n{}'
            print(fmt.format(self.options.user_data))
            sys.exit(1)

    def build_test_script(self):
        """Build test script"""
        platform = self.options.platform.lower()
        if platform:
            tbl = dict(unittest='create_unittest', pytest='create_pytest')
            method_name = tbl.get(platform, 'create_python_test')
            factory = RegexBuilder(
                user_data=self.options.user_data,
                test_data=self.options.test_data,
                **self.kwargs
            )
            factory.build()
            test_script = getattr(factory, method_name)()
            print('\n{}\n'.format(test_script))
            sys.exit(0)
        else:
            self.build_regex_pattern()

    def run_test(self):
        """Run test"""
        if self.options.test:
            factory = RegexBuilder(
                user_data=self.options.user_data,
                test_data=self.options.test_data,
                **self.kwargs
            )
            factory.build()
            test_result = factory.test(showed=True)
            print(test_result)
            sys.exit(0)

    def run(self):
        """Take CLI arguments, parse it, and process."""
        self.validate_cli_flags()
        run_gui_application(self.options)
        if not self.options.test_data:
            self.build_regex_pattern()
        self.run_test()
        self.build_test_script()


def execute():
    """Execute regexapp console CLI."""
    app = Cli()
    app.run()
