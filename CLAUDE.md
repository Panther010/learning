# CLAUDE.md - Learning Repository Handoff Document

## Repository Overview
- **Owner**: Bakul Seth, Lead Data Engineer targeting Principal/Staff level
- **Purpose**: Skills portfolio + learning space + interview prep reference
- **Tech stack**: Python 3.11, PySpark, SQL, pytest, pydantic
- **Time budget**: 5-7 hours/week
- **Cloud focus**: AWS first, then Azure, then GCP
- **Orchestration**: Airflow

## Current Progress
<!-- UPDATE THIS AFTER EVERY WORK SESSION -->
- **Current Phase**: Phase 1 - Foundation
- **Last completed task**: 1.1 Create .gitignore, 1.2 Create pyproject.toml (done by Claude during initial setup)
- **Last session date**: 2026-05-25
- **Next task to pick up**: 1.3 Remove tracked cache files from git
- **Notes**: .gitignore and pyproject.toml are created. Roadmap files are in docs/roadmap/. Start with task 1.3.

## Repository Structure
- `shared/` - Common modules (config, logging, spark session). ALL projects import from here. **You build this in Phase 1.**
- `data/` - ALL data files. `raw/` is checked in; `processed/` is gitignored. **You create this in Phase 1.**
- `fundamentals/` - Learning exercises. DS&A, SQL practice, Spark beginner. **You move existing files here in Phase 1.**
- `projects/` - Portfolio-grade projects. Each has config.yaml, src/, tests/, scripts/. **You migrate existing projects here in Phase 1.**
- `docs/roadmap/` - Phase-based task lists. Check boxes as you complete tasks. **You can amend these anytime.**
- `scripts/` - Utility scripts (git automation, migration helpers).

## Conventions (follow these for all new code)
- All Python files: snake_case filenames, type hints on all function signatures
- All PySpark jobs: import SparkSession from `shared.spark_session`, never create inline
- All file paths: resolved via `shared.config` or `shared.path_utils`, never hardcoded relative
- Logging: use `shared.logger.get_logger(__name__)`, never inline `logging.basicConfig`
- Config: each project has a `config.yaml`; loaded via `shared.config.load_project_config()`
- Tests: pytest, files named `test_*.py`, placed in `tests/` directory of each project
- SQL files: self-contained with CREATE TABLE, INSERT, and solution
- Commits: descriptive messages, one logical change per commit

## How to Resume Work (for Claude sessions)
1. Read this file to understand current state
2. Check `docs/roadmap/phase_XX_*.md` for the current phase's task list
3. Find the next unchecked task
4. User works on the task, comes back for review
5. After review: update "Current Progress" section above
6. Check off the completed task in the roadmap file

## Shared Module API Reference
**These modules don't exist yet — you build them in Phase 1 tasks 1.6-1.9**

### shared.path_utils (Task 1.6)
- `get_project_root() -> Path` - Returns repo root directory (finds pyproject.toml)
- `get_data_dir() -> Path` - Returns central data/ directory
- `get_raw_data_dir() -> Path` - Returns data/raw/
- `get_processed_data_dir() -> Path` - Returns data/processed/

### shared.logger (Task 1.7)
- `get_logger(name: str, level: str = "INFO") -> logging.Logger` - Returns configured logger

### shared.spark_session (Task 1.8)
- `get_or_create_spark(app_name: str, master: str, config: dict | None) -> SparkSession`
- `stop_spark() -> None`

### shared.config (Task 1.9)
- `load_project_config(project_name: str) -> ProjectConfig` - Loads project-specific config.yaml
- `ProjectConfig` - Pydantic model with spark, data_paths, input_files, output_dir fields

## Known Issues / Tech Debt
- Parquet output files (silver/gold) are still tracked in git — remove in task 1.3
- 40+ hardcoded relative paths across all Python files — migrate in tasks 1.12-1.13
- BST search method has a bug (missing return on recursive calls) — fix when enhancing DS&A
- `camel_to_snake` is implemented differently in 2 files with different bugs — consolidate into shared/
- `ingest_bronze.py` is a 289-line dump reading 4 unrelated datasets — needs splitting
 