from regexapp import version as expected_version
from subprocess import check_output
from subprocess import STDOUT
import re


def test_installed_version_synchronization():
    output = check_output('pip freeze', stderr=STDOUT, shell=True)
    if isinstance(output, bytes):
        output = output.decode()
    else:
        output = str(output)

    installed_version = ''
    pat = r'regexapp==(?P<version>[0-9]+(\.[0-9]+)*)$'
    for line in output.splitlines():
        match = re.match(pat, line.strip())
        if match:
            installed_version = match.group('version')
            break

    if installed_version:
        assert installed_version == expected_version
    else:
        assert False, output
