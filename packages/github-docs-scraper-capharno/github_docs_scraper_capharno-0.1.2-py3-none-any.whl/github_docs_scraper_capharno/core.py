"""
Core functionality for GitHub Documentation Scraper.
"""

from fnmatch import fnmatch
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse

import requests


def parse_github_url(url: str) -> Tuple[str, str, str]:
    """
    Parse GitHub URL into owner, repo, and path components.

    Correctly handles URLs with branch specifications like:
    - https://github.com/owner/repo/tree/main/path
    - https://github.com/owner/repo/blob/master/path
    """
    # Remove trailing slashes and .git extension
    url = url.rstrip("/").rstrip(".git")

    # Parse URL into components
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.split("/") if p]

    if len(path_parts) < 2:
        raise ValueError("URL must contain owner and repository name")

    owner = path_parts[0]
    repo = path_parts[1]

    # Handle tree/blob references to branches
    # GitHub URLs format: /owner/repo/tree/branch/path or /owner/repo/blob/branch/path
    path = ""
    if len(path_parts) > 2:
        if path_parts[2] in ("tree", "blob") and len(path_parts) > 3:
            # Skip the tree/blob part and the branch name to get the actual path
            path = "/".join(path_parts[4:]) if len(path_parts) > 4 else ""
        else:
            # Standard path without tree/blob reference
            path = "/".join(path_parts[2:])

    return owner, repo, path


def get_github_headers(token: Optional[str] = None) -> dict:
    """Get headers for GitHub API requests."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def should_exclude_file(filename: str, exclude_patterns: List[str]) -> bool:
    """
    Check if a file should be excluded based on glob patterns.

    Args:
        filename: Name of the file to check
        exclude_patterns: List of glob patterns to match against

    Returns:
        True if the file should be excluded, False otherwise
    """
    return any(
        fnmatch(filename.lower(), pattern.lower()) for pattern in exclude_patterns
    )


def get_docs_files(
    owner: str, repo: str, path: str, exclude: List[str], token: Optional[str] = None
) -> List[dict]:
    """Get list of markdown files from GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = get_github_headers(token)

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    files = response.json()
    return [
        file
        for file in files
        if file["name"].endswith(".md")
        and not should_exclude_file(file["name"], exclude)
    ]


def get_file_content(file_url: str, token: Optional[str] = None) -> str:
    """Fetch content of a single file from GitHub."""
    headers = get_github_headers(token)
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    return response.text


def save_files(
    files: List[dict], output_path: Path, token: Optional[str] = None
) -> None:
    """Save multiple files to the specified directory."""
    for file in files:
        content = get_file_content(file["download_url"], token)
        file_path = output_path / file["name"]

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


def combine_files(
    files: List[dict], output_file: Path, token: Optional[str] = None
) -> None:
    """Combine multiple files into a single output file."""
    with open(output_file, "w", encoding="utf-8") as outfile:
        for i, file in enumerate(files):
            content = get_file_content(file["download_url"], token)

            # Add separator between files
            if i > 0:
                outfile.write("\n\n---\n\n")

            # Write file content
            outfile.write(content)
