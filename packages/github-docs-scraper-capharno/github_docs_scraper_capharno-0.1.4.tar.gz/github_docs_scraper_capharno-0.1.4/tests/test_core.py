"""Tests for the core functionality of GitHub Documentation Scraper."""

import pytest

from github_docs_scraper_capharno.core import parse_github_url


def test_parse_github_url():
    """Test parsing of GitHub URLs."""
    # Test a basic URL
    owner, repo, path = parse_github_url("https://github.com/owner/repo/path/to/docs")
    assert owner == "owner"
    assert repo == "repo"
    assert path == "path/to/docs"

    # Test a URL with trailing slash
    owner, repo, path = parse_github_url("https://github.com/owner/repo/path/to/docs/")
    assert owner == "owner"
    assert repo == "repo"
    assert path == "path/to/docs"

    # Test a URL without a path
    owner, repo, path = parse_github_url("https://github.com/owner/repo")
    assert owner == "owner"
    assert repo == "repo"
    assert path == ""

    # Test a URL with .git extension
    owner, repo, path = parse_github_url("https://github.com/owner/repo.git")
    assert owner == "owner"
    assert repo == "repo"
    assert path == ""

    # Test a malformed URL
    with pytest.raises(ValueError):
        parse_github_url("https://github.com/owner")
