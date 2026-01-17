"""
Unit tests for the `textfsmgen.config` module.

Usage
-----
Run pytest in the project root to execute these tests:
    $ pytest tests/unit/test_config.py
    or
    $ python -m pytest tests/unit/test_config.py
"""

import pytest
from regexapp import version

from pathlib import Path
from pathlib import PurePath

import regexapp.config as config
from regexapp.deps import genericlib_shell_module as shell


# Package info for regexapp
pkg_info = shell.PackageInfo("regexapp")

# Skip marker if regexapp is not installed
skip_if_missing_regexapp = pytest.mark.skipif(
    not pkg_info.is_installed,
    reason="Skipping: regexapp package is not installed."
)


@skip_if_missing_regexapp
def test_version_matches_config():
    """Ensure installed package version matches config version."""
    assert pkg_info.is_installed is True
    assert pkg_info.version == config.version


class TestData:
    """Tests for Data class."""

    def test_user_reference_filename(self):
        """Check template filename path."""
        expected = str(PurePath(Path.home(), '.regexapp', 'user_references.yaml'))
        assert config.Data.user_reference_filename == expected

    def test_main_app_text(self):
        """Check main app text."""
        assert f"v{version}" in config.Data.main_app_text

    @pytest.mark.parametrize(
        "attr",
        [
            "genericlib",
            "pyyaml",
        ],
    )
    def test_package_texts(self, attr):
        """Check package text strings."""
        expected = f"{attr} v"
        assert getattr(config.Data, f"{attr}_text").lower().startswith(expected)

    @pytest.mark.parametrize(
        "attr",
        [
            "genericlib",
            "pyyaml",
        ],
    )
    def test_package_links(self, attr):
        """Check package links."""
        expected = f"https://pypi.org/project/{attr}"
        assert getattr(config.Data, f"{attr}_link").rstrip("/").lower() == expected

    def test_company_info(self):
        """Check company info."""
        assert config.Data.company == "Geeks Trident LLC"
        assert "geekstrident.com" in config.Data.company_url

    def test_repo_and_docs_urls(self):
        """Check repo and docs URLs."""
        assert config.Data.repo_url.startswith("https://github.com/")
        assert config.Data.documentation_url.endswith("README.md")
        assert config.Data.license_url.endswith("LICENSE")

    def test_license_info(self):
        """Check license info."""
        assert "RegexApp License" in config.Data.license_name
        assert "2022" in config.Data.copyright_text
        assert isinstance(config.Data.license, str)

    @pytest.mark.parametrize(
        "pkg",
        [
            "genericlib",
            "pyyaml",
        ],
    )
    def test_get_dependency(self, pkg):
        """Check dependency dict."""
        pkg_name, pkg_url = config.Data.get_dependency().get(pkg).values()
        assert pkg_name.startswith(f"{pkg} v")
        assert pkg_url.rstrip("/").lower() == f"https://pypi.org/project/{pkg}"

    def test_get_app_keywords(self):
        """Check app keywords retrieval."""
        assert "# file: system_references.yaml" in config.Data.get_app_keywords()

    def test_get_defined_symbols(self):
        """Check defined symbols retrieval."""
        assert "# file: symbols.yaml" in config.Data.get_defined_symbols()


    def test_get_user_custom_keywords(self):
        """Check user custom keywords retrieval."""
        content = config.Data.get_user_custom_keywords()
        if content:
            for expected in [
                "# Custom keywords are created by various end-users.",
                "# Ask maintainer to add new custom keyword.",
                "# Geeks Trident LLC has NO LICENSE RIGHT to these keywords."
            ]:
                assert expected in content
