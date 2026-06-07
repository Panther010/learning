# Phase 1: Foundation

**Target**: Weeks 1-6 | ~36 hours total | 5-7 hrs/week

<!--
AMENDABLE: Add, remove, or reorder tasks freely.
To add a task: copy the template at the bottom and fill in details.
To skip a task: change [ ] to [~] and add "SKIPPED: reason"
To add a custom topic: create docs/roadmap/custom_your_topic.md
-->

## Goals
- Clean git hygiene (ignore files, remove tracked artifacts)
- Shared modules to eliminate hardcoded paths and duplication
- Reorganize repo into portfolio-ready structure
- Machine-independent setup with `pip install -e .`

## Tasks

### 1.1 Create .gitignore
- [x] **Status: Completed**
- **What to do**: Create comprehensive .gitignore for Python, PySpark, IDE files, and data outputs.
- **What to learn**: Git ignore patterns. Why __pycache__, .crc, _SUCCESS files shouldn't be tracked.
- **Deliverable**: `.gitignore` at repo root
- **Estimated time**: 15 minutes
- **Come back for review**: No

### 1.2 Create pyproject.toml
- [x] **Status: Completed**
- **What to do**: Create pyproject.toml with project metadata, dependencies, and tool configuration.
- **What to learn**: Modern Python packaging (PEP 517/518). How pyproject.toml replaces setup.py. Dependency management. Tool configuration (pytest, ruff, mypy).
- **Deliverable**: `pyproject.toml` with dependencies (pyspark, pydantic, pyyaml, requests), dev dependencies (pytest, ruff, mypy), and tool configs
- **Estimated time**: 30 minutes
- **Come back for review**: No

### 1.3 Remove tracked cache files from git
- [ ] **Status: Not Started**
- **What to do**: Remove __pycache__ directories and Spark output files (.crc, _SUCCESS, parquet files) from git tracking.
- **What to learn**: `git rm -r --cached` command. Difference between deleting files vs untracking them. How .gitignore only affects untracked files.
- **Research**: Run `git status` to see what's tracked. Use `find . -name "__pycache__"` and `find . -name "*.crc"` to locate files.
- **Deliverable**: Clean `git status` with no cache files. Commit titled "Remove tracked cache and output files"
- **Acceptance criteria**: Run `git ls-files | grep -E '__pycache__|\.crc|_SUCCESS'` returns nothing
- **Estimated time**: 20 minutes
- **Come back for review**: No

### 1.4 Create directory structure
- [ ] **Status: Not Started**
- **What to do**: Create all target directories: `shared/`, `fundamentals/`, `projects/`, `data/`, `docs/`, `scripts/`
- **What to learn**: Why separate learning exercises from portfolio projects. Principle of organizing code by purpose, not by file type.
- **Deliverable**: Directory structure as documented in CLAUDE.md
- **Estimated time**: 10 minutes
- **Come back for review**: No

### 1.5 Organize data files
- [ ] **Status: Not Started**
- **What to do**: Move all data files to `data/raw/` or `data/streaming/`. Create `data/processed/.gitkeep`. Delete committed output parquet files.
- **What to learn**: Why centralize data in one location. Git vs local-only data storage patterns.
- **Research**: Use `find . -name "*.csv" -o -name "*.json" -o -name "*.parquet"` to locate data files
- **Deliverable**: All input data in `data/raw/`, streaming data in `data/streaming/`, `data/processed/.gitkeep` created
- **Estimated time**: 30 minutes
- **Come back for review**: No

### 1.6 Build shared/path_utils.py
- [ ] **Status: Not Started**
- **What to do**: Create `shared/path_utils.py` with functions: `get_project_root()`, `get_data_dir()`, `get_raw_data_dir()`, `get_processed_data_dir()`
- **What to learn**: How to find project root by walking up directory tree. `pathlib.Path` API. Why absolute paths are better than relative paths. How to make code work from any working directory.
- **Research**: Python pathlib documentation. Pattern: start from `__file__`, walk up until you find `pyproject.toml`
- **Deliverable**: `shared/path_utils.py` with 4 functions and docstrings
- **Acceptance criteria**: `from shared.path_utils import get_project_root; print(get_project_root())` prints correct path
- **Estimated time**: 1 hour
- **Come back for review**: Yes

### 1.7 Build shared/logger.py
- [ ] **Status: Not Started**
- **What to do**: Create `shared/logger.py` with `get_logger(name, level="INFO")` function.
- **What to learn**: Python logging module. Logger hierarchy. Why configure once, use everywhere. Format strings for logging. Log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- **Research**: Python logging documentation. Pattern: configure root logger once, return named loggers
- **Deliverable**: `shared/logger.py` with `get_logger()` function. Format: `[%(asctime)s] %(levelname)s - %(name)s - %(message)s`
- **Acceptance criteria**: `logger = get_logger(__name__); logger.info("test")` prints formatted message
- **Estimated time**: 1 hour
- **Come back for review**: Yes

### 1.8 Build shared/spark_session.py
- [ ] **Status: Not Started**
- **What to do**: Create `shared/spark_session.py` with `get_or_create_spark(app_name, master="local[*]", config=None)` and `stop_spark()`.
- **What to learn**: SparkSession singleton pattern. Why reusing SparkSession matters. How to configure Spark programmatically. Clean shutdown importance.
- **Research**: PySpark SparkSession documentation. Pattern: check if session exists, create if not, apply config
- **Deliverable**: `shared/spark_session.py` with 2 functions
- **Acceptance criteria**: Calling `get_or_create_spark()` twice returns the same session object
- **Estimated time**: 1.5 hours
- **Come back for review**: Yes

### 1.9 Build shared/config.py
- [ ] **Status: Not Started**
- **What to do**: Create `shared/config.py` with pydantic `ProjectConfig` model and `load_project_config(project_name)` function.
- **What to learn**: Pydantic for configuration validation. YAML parsing. Why typed config is better than raw dicts. Config-driven development pattern.
- **Research**: Pydantic BaseModel documentation. Pattern: read YAML from `projects/{name}/config.yaml`, validate with pydantic
- **Deliverable**: `shared/config.py` with ProjectConfig model (fields: project_name, spark, data_paths, input_files, output_dir) and load function
- **Acceptance criteria**: Can load a sample config.yaml and access fields with autocomplete
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 1.10 Write tests for shared modules
- [ ] **Status: Not Started**
- **What to do**: Create `shared/tests/test_path_utils.py`, `test_logger.py`, `test_spark_session.py`, `test_config.py`
- **What to learn**: pytest basics. How to test pure functions vs stateful objects. Mocking file system operations. Testing logging output. Testing SparkSession creation.
- **Research**: pytest documentation. Pattern: one test file per module, test happy path + edge cases
- **Deliverable**: 4 test files in `shared/tests/`. All tests pass with `pytest shared/tests/ -v`
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 1.11 Move fundamentals files
- [ ] **Status: Not Started**
- **What to do**: Use `git mv` to move DS&A, exercises, numpy, SQL, Spark files to `fundamentals/`. Normalize filenames to snake_case. Fix tree file typo (impliment -> implement).
- **What to learn**: `git mv` preserves history. File naming conventions matter for imports. Why normalize early.
- **Research**: Run `ls -R Python/ Pyspark/ SQL/` to see current structure
- **Deliverable**: All learning exercises in `fundamentals/` subdirectories. Clean git history.
- **Estimated time**: 1.5 hours
- **Come back for review**: Yes

### 1.12 Move project files
- [ ] **Status: Not Started**
- **What to do**: Use `git mv` to move flight_analysis, banking_pipeline, yelp_analysis, world_bank_gdp to `projects/`. Move github_automation.py to `scripts/`.
- **What to learn**: Separating portfolio projects from exercises. Why project structure matters for presentation.
- **Deliverable**: All portfolio projects in `projects/` subdirectories
- **Estimated time**: 30 minutes
- **Come back for review**: No

### 1.13 Create config.yaml for each project
- [ ] **Status: Not Started**
- **What to do**: Create `config.yaml` in each project directory declaring input files and output directories.
- **What to learn**: Declarative configuration. Separation of code and config. Why this makes projects portable.
- **Research**: Look at existing project code to identify hardcoded paths and file references
- **Deliverable**: `projects/*/config.yaml` for each of 4 projects
- **Estimated time**: 1 hour
- **Come back for review**: Yes

### 1.14 Delete per-project duplicated modules
- [ ] **Status: Not Started**
- **What to do**: Delete `logger.py` and `spark_manager.py` from individual project directories (now replaced by shared/).
- **What to learn**: DRY principle in practice. Why centralized modules beat copy-paste.
- **Deliverable**: No more duplicated logger.py or spark_manager.py files
- **Estimated time**: 10 minutes
- **Come back for review**: No

### 1.15 Migrate hardcoded paths in all files
- [ ] **Status: Not Started**
- **What to do**: Replace all hardcoded relative paths with shared module calls. Replace inline SparkSession creation with `get_or_create_spark()`. Replace inline logging with `get_logger()`.
- **What to learn**: Large-scale refactoring patterns. Search/replace with verification. Why this migration pays off long-term.
- **Research**: Use `grep -rn '\.\./\.\.' --include="*.py"` to find hardcoded paths. Use `grep -rn "master('local')" --include="*.py"` to find inline Spark sessions.
- **Deliverable**: Zero hardcoded paths. All Spark sessions use shared module. All logging uses shared module.
- **Acceptance criteria**: `grep -rn '\.\./\.\.' --include="*.py"` returns 0 matches
- **Estimated time**: 4 hours (largest task in Phase 1)
- **Come back for review**: Yes (in chunks - review per project)

### 1.16 Install, verify, and commit
- [ ] **Status: Not Started**
- **What to do**: Run `pip install -e .`. Run `pytest shared/tests/ -v`. Run one project end-to-end (flight_analysis). Verify all tests pass. Create final commit.
- **What to learn**: Editable install pattern. End-to-end verification. Why testing after refactoring is critical.
- **Deliverable**: Working installation. All tests green. At least one project runs successfully.
- **Acceptance criteria**: `pytest shared/tests/ -v` passes. `python projects/flight_analysis/scripts/run_pipeline.py` succeeds.
- **Estimated time**: 1 hour
- **Come back for review**: Yes

---

## Task Template (copy this to add new tasks)

### 1.XX Task Title
- [ ] **Status: Not Started**
- **What to do**: Description of the task
- **What to learn**: Key concepts and skills
- **Research**: Where to look for information
- **Deliverable**: What gets created or modified
- **Acceptance criteria**: How to verify completion
- **Estimated time**: X hours
- **Come back for review**: Yes/No

---

## Total Estimated Time: ~36 hours
- Shared modules build + tests: ~9 hours
- File migration + organization: ~3.5 hours
- Hardcoded path migration: ~4 hours
- Config creation + verification: ~2 hours
- Infrastructure: ~1.5 hours

## Progress Tracking
Update CLAUDE.md's "Current Progress" section after completing each task.
