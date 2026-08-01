# Repository Guidelines

## Project Structure & Module Organization

This repository is a data-engineering learning workspace and portfolio. Keep new work in the most appropriate area:

- `fundamentals/` holds current Python and Spark exercises and interview-prep solutions.
- `Pyspark/` and `Python/` preserve older learning material and basic projects; avoid broad refactors there unless the task requires one.
- `SQL/questions_and_solution_*/` contains self-contained SQL interview problems.
- `data/raw/` contains source datasets; generated output belongs in `data/processed/` (and should not be committed).
- `shared/` is the reusable package for paths, logging, and Spark-session management.
- `Documents/` holds theory, project design, and the phase roadmaps in `Documents/docs/Roadmap/`.

New portfolio-grade projects should move toward `projects/<project_name>/`, with `src/`, `tests/`, configuration, and a README.

## Build, Test, and Development Commands

Use Python 3.11 or newer and install the project with development dependencies:

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
mypy shared fundamentals
```

`pytest` uses the paths configured in `pyproject.toml`: `shared/tests`, `projects`, and `fundamentals`. Run an individual test with `pytest path/to/test_file.py`. Run Spark jobs from their project directory when legacy imports or relative paths require it.

## Coding Style & Naming Conventions

Use four-space indentation, Python type hints for new or changed functions, `snake_case` modules/functions/variables, and `PascalCase` classes. Keep lines within Ruff's 120-character limit. Use `ruff check .` before submitting changes.

For new Spark code, use `shared.spark_session.get_or_create_spark()` rather than building an inline session; use `shared.logger.get_logger(__name__)`; and resolve repository data paths with `shared.path_utils` instead of hardcoded relative paths. Keep SQL files self-contained with setup DDL, sample data, and a solution.

## Testing Guidelines

Write pytest tests named `test_*.py` in the nearest `tests/` directory. Test transformation logic independently where possible; Spark tests should create and stop a local session cleanly. Add regression tests when fixing a bug. There is no repository-wide coverage threshold yet.

## Commit & Pull Request Guidelines

Recent history uses short descriptive commits, often `Auto-commit for <scope>`; prefer clearer imperative messages such as `Add flight ingestion schema validation`. Keep each commit focused. Pull requests should state the purpose, list validation commands run, link relevant work where applicable, and include screenshots only for documentation or visual-output changes.

## Data and Configuration Safety

Do not commit credentials, API keys, generated Spark outputs, virtual environments, or large new datasets without agreement. Keep sample data small and document any required external setup in the project README.
