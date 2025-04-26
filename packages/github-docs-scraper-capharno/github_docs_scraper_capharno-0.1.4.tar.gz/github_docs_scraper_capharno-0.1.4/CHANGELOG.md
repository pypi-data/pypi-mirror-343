# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-04-25

### Added

- Initial release
- CLI interface with Click
- Markdown file scraping from GitHub repositories
- File combining and saving options
- File exclusion using glob patterns
- JSON output with file metadata and content (`-j/--json` flag)
- Verbose logging support (`-v/--verbose` flag)
- GitHub token authentication support
- Proper handling of GitHub repository URLs with branch indicators (tree/main)
- Version information via `--version` flag