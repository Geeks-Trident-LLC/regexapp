from regexapp import version as expected_version
from subprocess import check_output
from subprocess import STDOUT
import re
from pathlib import PurePath

from regexapp import LinePattern
from regexapp.config import Data

import pytest       # noqa


def get_package_info(pkg_name):
    """return package name from pip freeze command line"""
    output = check_output('pip freeze', stderr=STDOUT, shell=True)
    if isinstance(output, bytes):
        output = output.decode()
    else:
        output = str(output)

    found = [l.strip() for l in output.splitlines() if l.startswith(pkg_name)]  # noqa
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
    match = re.match(pattern, pkg_info.strip())     # noqa
    if match:
        installed_version = match.group('version')
        assert installed_version == expected_version, pkg_info
    else:
        assert False, pkg_info


@pytest.mark.parametrize(
    'pkg',
    [
        'pyyaml'
    ]
)
def test_package_dependencies(pkg):
    pypi_project_url = 'https://pypi.org/project'

    attrs = dir(Data)

    expected_pkg_link = str(PurePath(pypi_project_url, pkg)).lower()

    is_matched = False
    for attr in attrs:
        if attr.endswith('_text'):
            pkg_txt = getattr(Data, attr)
            if pkg_txt.lower().startswith(pkg.lower()):
                pkg_link = getattr(Data, attr.replace('_text', '_link'))
                pkg_link = str(PurePath(pkg_link)).lower()
                assert pkg_link == expected_pkg_link
                is_matched = True
    else:
        assert is_matched
