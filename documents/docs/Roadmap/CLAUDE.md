# CLAUDE.md - Learning Repository Handoff Document

## Repository Overview
- **Owner**: Bakul Seth, Lead Data Engineer targeting Principal/Staff level
- **Purpose**: Skills portfolio + learning space + interview prep reference
- **Tech stack**: Python 3.11, PySpark, SQL, pytest, pydantic
- **Time budget**: 5-7 hours/week
- **Cloud focus**: AWS first, then Azure, then GCP
- **Orchestration**: Airflow

## Current Progress
- **Current Phase**: Phase 0 - Interview Prep (NEW - URGENT)
- **Last completed task**: Created Phase 0 roadmap
- **Last session date**: 2026-06-07
- **Next task to pick up**: Phase 0, Week 1, Day 1 (see roadmap)
- **Notes**: Resigning this week. Phase 0 front-loads interview prep (4 weeks, 7-8 hrs/day) while building 6 portfolio projects. All work commits to this repo. After Phase 0, resume Phase 1-6.

## Repository Structure

### Current State (Before Phase 1 Completion)
```
learning/
├── .gitignore
├── pyproject.toml
├── CLAUDE.md (this file)
├── Python/         # To be moved to fundamentals/python/
├── Pyspark/        # To be moved to fundamentals/spark/ and projects/
├── SQL/            # To be moved to fundamentals/sql/
└── data/           # Already created, will be organized
```

### Target State (After Phase 1 Completion)
```
learning/
├── CLAUDE.md                    # Claude handoff document
├── README.md                    # Portfolio landing page
├── pyproject.toml               # Dependencies + tool config
├── .gitignore                   # Ignore caches, output, IDE
├── .pre-commit-config.yaml      # ruff (added in Phase 2)
├── conftest.py                  # Root pytest config + SparkSession fixture
├── Makefile                     # Common commands
│
├── shared/                      # Common importable modules
│   ├── __init__.py
│   ├── path_utils.py
│   ├── config.py
│   ├── logger.py
│   ├── spark_session.py
│   └── tests/
│
├── data/                        # ALL data files (single location)
│   ├── raw/                     # Source files (checked in, small ones)
│   ├── processed/               # Pipeline output (gitignored)
│   └── streaming/               # Streaming test data
│
├── fundamentals/                # Learning exercises (NOT portfolio)
│   ├── python/
│   │   ├── ds_and_algo/         # Existing DS&A (keep + enhance)
│   │   ├── exercises/           # Existing basics
│   │   ├── numpy/               # Existing numpy
│   │   └── projects/            # Small skill projects
│   ├── spark/
│   │   ├── beginner_exercises/  # Existing 9 exercises
│   │   ├── streaming/           # Existing batch_word_count
│   │   ├── optimization/        # New in Phase 3
│   │   ├── delta_lake/          # New in Phase 3
│   │   └── sql_in_spark/        # New in Phase 3
│   └── sql/
│       ├── README.md            # Index of all problems by topic
│       ├── set_01/              # Existing 26 problems
│       ├── set_02/              # Existing 24 problems
│       └── set_03/              # Existing 2+ problems
│
├── projects/                    # Portfolio-grade projects
│   ├── flight_analysis/         # Existing (refactored)
│   ├── banking_pipeline/        # Existing (refactored)
│   ├── yelp_analysis/           # Existing (refactored)
│   ├── world_bank_gdp/          # Existing (refactored)
│   └── (future projects here)
│
├── scripts/                     # Utility scripts
│   └── github_automation.py
│
└── docs/
    ├── roadmap/                 # Phase-based task lists (amendable)
    │   ├── phase_01_foundation.md
    │   ├── phase_02_python_engineering.md
    │   ├── phase_03_spark_depth.md
    │   ├── phase_04_end_to_end_project.md
    │   ├── phase_05_orchestration.md
    │   ├── phase_06_cloud_aws.md
    │   └── ongoing_practice.md
    ├── adr/                     # Architecture Decision Records
    └── notes/                   # Learning notes, cheat sheets
```

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
```python
from shared.path_utils import get_project_root, get_data_dir, get_raw_data_dir, get_processed_data_dir

# Returns repo root directory (finds pyproject.toml)
root = get_project_root()

# Returns central data/ directory
data = get_data_dir()

# Returns data/raw/
raw = get_raw_data_dir()

# Returns data/processed/
processed = get_processed_data_dir()
```

### shared.logger (Task 1.7)
```python
from shared.logger import get_logger

# Returns configured logger with timestamp+level+module format
logger = get_logger(__name__)
logger.info("Processing started")
```

### shared.spark_session (Task 1.8)
```python
from shared.spark_session import get_or_create_spark, stop_spark

# Get or create SparkSession
spark = get_or_create_spark(
    app_name="MyApp",
    master="local[*]",
    config={"spark.sql.shuffle.partitions": "4"}
)

# Clean shutdown
stop_spark()
```

### shared.config (Task 1.9)
```python
from shared.config import load_project_config

# Loads config.yaml from project directory
config = load_project_config("flight_analysis")

# Access configuration
input_file = config.resolve_input("flights_data")  # Resolves to full path
output_dir = config.resolve_output("silver")
spark_config = config.spark
```

## Known Issues / Tech Debt
- Parquet output files (silver/gold) are still tracked in git — remove in task 1.3
- 40+ hardcoded relative paths across all Python files — migrate in tasks 1.12-1.13
- BST search method has a bug (missing return on recursive calls) — fix when enhancing DS&A
- `camel_to_snake` is implemented differently in 2 files with different bugs — consolidate into shared/
- `ingest_bronze.py` is a 289-line dump reading 4 unrelated datasets — needs splitting

## Learning Resources
- Plan document: `/Users/bakulseth/.claude/plans/floofy-percolating-cascade.md`
- Roadmap files: `docs/roadmap/phase_*.md`
- Progress tracking: Update this file's "Current Progress" section after each completed task

## Roadmap Amendment Process
You can amend any roadmap file at any time:
- Add new tasks by copying the task template
- Skip tasks by changing `[ ]` to `[~]` and adding `SKIPPED: reason`
- Reorder tasks within a phase
- Create new phase files: `phase_07_azure.md`, `custom_kafka_deep_dive.md`, etc.
- Update this file's "Current Progress" to point to any task in any phase

Each roadmap file has detailed instructions in its header on how to amend it.
