# Contributing to GitHub Documentation Scraper

Thank you for considering contributing to GitHub Documentation Scraper!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/github-docs-scraper.git`
3. Set up a virtual environment using uv:
   ```bash
   pip install uv
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install in development mode:
   ```bash
   uv add -e . --dev
   ```

## Development Workflow

1. Create a new branch for your feature: `git checkout -b feature-name`
2. Make your changes
3. Format and lint your code:
   ```bash
   ruff format .
   ruff check .
   ```
4. Run the type checker:
   ```bash
   pyright
   ```
5. Run tests:
   ```bash
   pytest
   ```
6. Commit your changes using commitizen:
   ```bash
   cz commit
   ```
7. Push to your fork: `git push origin feature-name`
8. Create a pull request

## Commit Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for our commit messages. This helps us automate versioning and changelog generation.

Use `cz commit` to create properly formatted commits. The commit message format should be:

```
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

### Common types:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Changes that don't affect code meaning (formatting)
- **refactor**: Code changes that neither fix bugs nor add features
- **perf**: Performance improvements
- **test**: Adding or fixing tests
- **build**: Changes affecting the build system or dependencies
- **ci**: Changes to CI configuration files and scripts

For breaking changes, add a `!` after the type/scope or add "BREAKING CHANGE:" in the footer.

## Versioning

We use [Semantic Versioning](https://semver.org/) and automatically determine version bumps from commit messages:

- `fix:` commit → PATCH bump (1.0.0 → 1.0.1)
- `feat:` commit → MINOR bump (1.0.0 → 1.1.0)
- `feat!:` or commit with `BREAKING CHANGE:` → MAJOR bump (1.0.0 → 2.0.0)

Maintainers handle version bumping and releases.

## Code Style

We use Ruff for linting and formatting. Make sure your code passes all linting checks before submitting a pull request.

## Testing

All new features should include tests. We use pytest for testing.

## Documentation

Update the README.md if you add new features or change existing behavior.

## Pull Request Process

1. Update the README.md with details of your changes, if applicable
2. The CI pipeline must pass for your changes to be considered
3. Wait for review and approval from maintainers 