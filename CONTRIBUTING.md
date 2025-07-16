# Contributing to Open RAG Bot

![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

Thanks for your interest in contributing!
See [README.md](./README.md) for project overview.

This guide outlines the steps to contribute code, documentation, or ideas.

## Getting Started

1. **Fork the repository** and clone your fork.
2. **Install dependencies**:
   ```bash
   pip install pdm
   pdm install
   ```
3. Copy and configure environment variables:
   ```bash
   cp ./.env.example ./.env
   # Add your API keys
   ```

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

Before committing code, run:

```bash
pdm run ruff check src/ tests/
pdm run ruff format src/ tests/
```

We follow:

- [PEP8](https://peps.python.org/pep-0008/)
- [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

## Testing

Tests are written with `pytest`.

To run all tests:

```bash
pdm run pytest
```

You can write tests under the `tests/` folder.

## Pre-commit Hooks

Install pre-commit to automatically check formatting and linting before every commit:

```bash
pdm add --dev pre-commit  # one-time setup
pdm run pre-commit install
```

You can manually run all hooks with:

```bash
pdm run pre-commit run --all-files
```

## Contributing Workflow

1. Create a new branch for your change:
   ```bash
   git checkout -b <feature-or-fix-branch>
   ```
2. Make your changes and commit with a clear message:
   ```bash
   git commit -m "feat: short description of the change"
   ```
3. Push your branch and open a Pull Request:
   - Include a description of your changes
   - Link related issues if applicable
   - If it's a draft, mark it as such

## Pull Request Checklist

- [ ] All tests pass (`pdm run pytest`)
- [ ] Code is formatted and lints cleanly (`pdm run ruff check/format src/ tests/`)
- [ ] Pre-commit hooks have been run (`pdm run pre-commit run --all-files`)
- [ ] Relevant docstrings and comments updated
- [ ] README or docs updated if needed


## Types of Contributions

You're welcome to contribute:

- New features
- Bug fixes
- Documentation (README, docstrings)
- Tests
- Refactors
- Support for new LLM/embedding providers
- Translations (web UI)

# Communication & Support

- For questions or guidance, open a [GitHub Discussion](https://github.com/whitris/open-rag-bot/discussions) or issue.
- If you're working on a specific issue, feel free to comment and ask for clarification.

---

Thanks for helping improve Open RAG Bot!
