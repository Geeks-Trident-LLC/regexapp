from regexapp import version as expected_version
from subprocess import check_output
from subprocess import STDOUT
import re

from regexapp import LinePattern

import pytest


def get_package_info(pkg_name):
    """return package name from pip freeze command line"""
    output = check_output('pip freeze', stderr=STDOUT, shell=True)
    if isinstance(output, bytes):
        output = output.decode()
    else:
        output = str(output)

    found = [l.strip() for l in output.splitlines() if l.startswith(pkg_name)]
    if found:
        return found[0]
    else:
        return output


pkg_info = get_package_info('regexapp')

installed_pkg_check = pytest.mark.skipif(
    pkg_info.startswith('regexapp @ '),
    reason='skip because regexapp installed locally <<{}>>.'.format(pkg_info)
)


@installed_pkg_check
def test_installed_version_synchronization():
    pattern = LinePattern('data(regexapp==)mixed_word(var_version)end()')
    match = re.match(pattern, pkg_info.strip())
    if match:
        installed_version = match.group('version')
        assert installed_version == expected_version, pkg_info
    else:
        assert False, pkg_info
