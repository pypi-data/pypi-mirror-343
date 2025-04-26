# GitHub Documentation Scraper

A command-line tool to scrape markdown documentation from GitHub repositories.

## Features

- Scrape markdown files from any GitHub repository
- Combine files into a single document or save separately
- Output file metadata and content as JSON for programmatic use
- Exclude files using glob patterns (e.g., `*.draft.md`, `changelog.*`)
- GitHub token support for authenticated requests
- Progress indicators and colorful output
- Verbose debug logging for troubleshooting
- Proper handling of GitHub repository URLs with branch indicators (tree/main)

## Installation

```bash
# From PyPI
uv add github_docs_scraper_capharno

# From source
uv add install .
```

## Usage

```bash
# Basic usage (requires -o or -j)
scrape-docs https://github.com/owner/repo/docs -o combined.md

# Combine files into a single document
scrape-docs https://github.com/owner/repo/docs -o combined.md

# Save files separately
scrape-docs https://github.com/owner/repo/docs -s -o docs/

# Exclude files using glob patterns
scrape-docs https://github.com/owner/repo/docs -e "*.draft.md" -e "changelog.*" -o combined.md

# Use with GitHub token
scrape-docs https://github.com/owner/repo/docs -t your_token_here -o combined.md

# Output JSON metadata and content
scrape-docs https://github.com/owner/repo/docs -j

# Enable verbose logging
scrape-docs https://github.com/owner/repo/docs -v -o combined.md

# Combine JSON output with file saving
scrape-docs https://github.com/owner/repo/docs -j -o combined.md

# Display version information
scrape-docs --version

```shell
GitHub Docs Scraper, version 0.1.2
```

### Options

- `-o, --output PATH`: Output file or directory
- `-e, --exclude PATTERN`: Glob patterns for files to exclude (can be used multiple times)
- `-t, --token TEXT`: GitHub token (defaults to GITHUB_TOKEN env var)
- `-s, --separate`: Save files separately instead of combining
- `-j, --json`: Output JSON metadata and content to stdout
- `-v, --verbose`: Enable verbose debug logging
- `--version`: Show version information
- `--help`: Show help message

## JSON Output

The `-j/--json` flag outputs structured JSON data containing metadata and content for each markdown file. This is useful for programmatic processing or integration with other tools.

### JSON Format

Each file is represented as a JSON object with the following properties:

```json
{
  "name": "example.md",
  "path": "docs/example.md",
  "download_url": "https://raw.githubusercontent.com/owner/repo/main/docs/example.md",
  "size": 1234,
  "type": "file",
  "html_url": "https://github.com/owner/repo/blob/main/docs/example.md",
  "content": "# Example\n\nThis is the raw markdown content..."
}
```

### Using JSON Output in Scripts

When using the JSON flag, all logs are directed to stderr, ensuring that stdout contains only the JSON data. This makes it easy to pipe the output to other tools:

```bash
# Save JSON to a file
scrape-docs https://github.com/owner/repo/docs -j > docs.json

# Redirect logs to a separate file
scrape-docs https://github.com/owner/repo/docs -j > docs.json 2> logs.txt

# Process JSON with jq
scrape-docs https://github.com/owner/repo/docs -j | jq '.[].name'

# Count the number of files
scrape-docs https://github.com/owner/repo/docs -j | jq 'length'

# Extract just the content from a specific file
scrape-docs https://github.com/owner/repo/docs -j | jq '.[] | select(.name=="README.md") | .content'
```

## Verbose Logging

The `-v/--verbose` flag enables detailed debug logs, which can be helpful for troubleshooting:

```bash
# Enable verbose logging
scrape-docs https://github.com/owner/repo/docs -v -o combined.md

# Combine verbose logging with JSON output (logs go to stderr)
scrape-docs https://github.com/owner/repo/docs -j -v > docs.json 2> debug.log
```

## Versioning

This project follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

You can check the current version with:

```bash
scrape-docs --version
```

Version information is also available programmatically:

```python
from github_docs_scraper_capharno import __version__
print(__version__) 
```

When upgrading between versions, check the [CHANGELOG.md](CHANGELOG.md) for details on what has changed.

## Development

1. Clone the repository
2. Create and activate a virtual environment
3. Install development dependencies:

    ```bash
    uv add -e . --dev
    ```

4. Run tests

```bash
pytest
```

5. Use conventional commits to make your changes:

```bash
cz commit
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on our development workflow and commit conventions.

## Release Process

This project uses `bump-my-version` and manual tagging for releases.

1.  **Determine the next version**
2.  **Update the version:**
    ```bash
    # Example for a patch release
    bump-my-version patch
    ```
    *   This updates the version in `pyproject.toml` (or other configured files) but **does not** commit or tag.
3.  **Stage the changes:**
    ```bash
    git add pyproject.toml # Or other files modified by bump-my-version
    ```
4.  **Commit the version bump:**
    ```bash
    # Use a commit message like "Bump version to X.Y.Z"
    git commit -m "Bump version to 0.1.27"
    ```
    *   Your pre-commit hooks will run at this stage. Ensure they pass.
5.  **Tag the commit:**
    ```bash
    git tag v0.1.27 # Use the same version number as the bump
    ```
6.  **Push the commit and the tag:**
    ```bash
    git push origin <your-branch> # Push the commit first
    git push origin v0.1.27      # Then push the tag
    ```
7.  **Automation takes over:** Pushing the `v*` tag triggers the "Publish Python Package" GitHub Actions workflow, which:
    *   Creates a GitHub Release with auto-generated notes.
    *   Builds the package.
    *   Publishes the package to TestPyPI and PyPI (if configured).

## Building

To build distribution packages:

```bash
# Build both wheel and source distribution
uv build

# The built packages will be in the dist/ directory
```

To install from the built distributions:

```bash
# Install from wheel (preferred)
uv add ./dist/github_docs_scraper_capharno-x.y.z-py3-none-any.whl

# Or install from source tarball
uv add ./dist/github_docs_scraper_capharno-x.y.z.tar.gz
```

## License

MIT
