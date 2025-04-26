#!/usr/bin/env python3
"""
GitHub Documentation Scraper CLI

A command-line tool to scrape markdown documentation from GitHub repositories.
Supports excluding specific files, custom output locations, and GitHub token
authentication.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Optional, Tuple

import click
from dotenv import load_dotenv

from github_docs_scraper_capharno import __version__
from github_docs_scraper_capharno.core import (
    combine_files,
    get_docs_files,
    get_file_content,
    parse_github_url,
    save_files,
)

# Load environment variables for default token
load_dotenv()

# Set up logger
logger = logging.getLogger("github_docs_scraper")


@click.command()
@click.argument("url", type=str)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    help="Glob patterns for files to exclude (can be used multiple times). "
    "Examples: *.draft.md, draft-*, changelog.*",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    help="Output file for combined docs or directory for individual files.",
)
@click.option(
    "-t",
    "--token",
    envvar="GITHUB_TOKEN",
    help="GitHub token (defaults to GITHUB_TOKEN environment variable)",
)
@click.option(
    "-s",
    "--separate",
    is_flag=True,
    help="Save files separately instead of combining them",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose debug logging",
)
@click.option(
    "-j",
    "--json",
    "json_output",
    is_flag=True,
    help="Output JSON metadata of fetched files to stdout (includes file content)",
)
@click.version_option(version=__version__, prog_name="GitHub Docs Scraper")
def main(
    url: str,
    exclude: Tuple[str],
    output: Optional[Path],
    token: Optional[str],
    separate: bool,
    verbose: bool,
    json_output: bool,
) -> None:
    """
    Scrape markdown documentation from a GitHub repository.

    URL should be in the format: https://github.com/owner/repo/path/to/docs

    Example:
    \b
        # Combine files into single document (requires -o)
        scrape-docs https://github.com/owner/repo/docs -o combined.md

        # Save files separately (requires -o)
        scrape-docs https://github.com/owner/repo/docs -s -o docs/

        # Exclude files using glob patterns
        scrape-docs https://github.com/owner/repo/docs -e "*.draft.md" \
        -e "changelog.*" -o combined.md

        # Output JSON metadata and content of files to stdout
        scrape-docs https://github.com/owner/repo/docs -j

        # Output JSON and also save to file
        scrape-docs https://github.com/owner/repo/docs -j -o combined.md
    """
    # Configure logging based on verbose flag and json output
    log_level = logging.DEBUG if verbose else logging.INFO

    # When using JSON output, direct logs only to stderr, not stdout
    if json_output:
        # Create a handler that outputs to stderr
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        # Configure the root logger to use our handler
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.handlers = []  # Remove any existing handlers
        root_logger.addHandler(stderr_handler)
    else:
        # Standard logging to stdout
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    try:
        # Parse GitHub URL
        logger.info(f"Parsing GitHub URL: {url}")
        owner, repo, path = parse_github_url(url)
        logger.debug(f"Parsed URL - Owner: {owner}, Repo: {repo}, Path: {path}")

        # Convert exclude tuple to list
        exclude_list = list(exclude)
        if exclude_list:
            logger.debug(f"Excluding files matching: {', '.join(exclude_list)}")

        # Get list of markdown files
        logger.info(f"Fetching markdown files from {owner}/{repo}/{path}")
        files = get_docs_files(owner, repo, path, exclude_list, token)
        logger.debug(f"Found {len(files)} markdown files")

        if not files:
            logger.warning("No markdown files found!")
            if not json_output:
                click.echo("No markdown files found!")
            else:
                # Still output empty JSON array when no files found
                click.echo("[]")
            return

        # Output JSON to stdout if requested
        if json_output:
            # Create a simplified representation with relevant metadata and content
            logger.info("Fetching file contents for JSON output")
            json_files = []
            for file in files:
                logger.debug(f"Fetching content for {file['name']}")
                content = get_file_content(file["download_url"], token)
                json_files.append(
                    {
                        "name": file["name"],
                        "path": file["path"],
                        "download_url": file["download_url"],
                        "size": file["size"],
                        "type": file["type"],
                        "html_url": file.get("html_url", ""),
                        "content": content,
                    }
                )
            click.echo(json.dumps(json_files, indent=2))

        # Check if output path is provided for file operations
        if not output and not json_output:
            logger.warning(
                "No output path specified. Use -o to write files or -j to output JSON."
            )
            click.echo(
                "No output path specified. Use -o to write files or -j to output JSON."
            )
            return

        # Only process files if output path is provided
        if output:
            output_path = Path(output)
            logger.debug(f"Output path: {output_path}")

            # Create output directory if saving separately
            if separate:
                logger.info(f"Saving files separately to {output_path}/")
                output_path.mkdir(exist_ok=True)
                save_files(files, output_path, token)
                logger.info(f"Successfully saved {len(files)} files")
                if not json_output:
                    click.echo(f"\n✨ All files saved to {output_path}/")
            else:
                logger.info(f"Combining files and saving to {output_path}")
                combine_files(files, output_path, token)
                logger.info(f"Successfully combined {len(files)} files")
                if not json_output:
                    click.echo(f"\n✨ Combined documentation saved to {output_path}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=verbose)
        if not json_output:
            click.echo(f"Error: {e}", err=True)
        else:
            # In JSON mode, we still want to report errors to stderr
            click.echo(f"Error: {e}", err=True)
            # Output an empty JSON array to stdout to maintain valid JSON output
            click.echo("[]")


if __name__ == "__main__":
    main()
