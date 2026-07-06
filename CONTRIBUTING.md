# Contributing to ThinkFlow Studio

Thank you for your interest in contributing to ThinkFlow Studio!

## Development Setup
1. Clone the repository
2. Run `make build` and `make run` to spin up the local Docker environment.
3. Use `make test` to run the test suite.

## Code Style
We enforce strict typing and code formatting. Before submitting a PR, run:
```bash
make audit
```
This will run `ruff` for linting and `mypy` for type checking.

## Pull Request Process
1. Fork the repo and create your branch from `main`.
2. Add tests for any new agent or orchestration feature.
3. Update the `docs/` and Mermaid diagrams if you alter the pipeline.
4. Ensure the test suite passes.
