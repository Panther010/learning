# Phase 2: Python Engineering Best Practices

**Target**: Weeks 7-12 | ~36 hours total | 5-7 hrs/week

<!--
AMENDABLE: Add, remove, or reorder tasks freely.
This phase focuses on production-grade Python: tests, types, patterns, tooling.
-->

## Goals
- Comprehensive pytest test coverage
- Type hints everywhere (mypy compliance)
- Design patterns in practice
- Code quality automation (ruff, pre-commit)
- Professional documentation

## Tasks

### 2.1 Add pytest to all DS&A problems
- [ ] **Status: Not Started**
- **What to do**: Write pytest tests for all data structures and algorithms. Each file should have a corresponding test file.
- **What to learn**: pytest fundamentals (fixtures, parametrize, assertions). Test organization. Testing algorithmic code (edge cases, correctness, complexity).
- **Research**: pytest documentation. Look at existing DS&A code to identify test cases.
- **Deliverable**: `fundamentals/python/ds_and_algo/tests/` with test coverage for all DS&A files
- **Estimated time**: 4 hours
- **Come back for review**: Yes

### 2.2 Add type hints to all Python files
- [ ] **Status: Not Started**
- **What to do**: Add type hints to all function signatures in the repo. Run mypy to verify correctness.
- **What to learn**: Python typing module (List, Dict, Optional, Union, TypeVar, Protocol). Why type hints improve code quality. How mypy catches bugs before runtime.
- **Research**: Python typing documentation. mypy documentation. Start with simple functions, work up to generics.
- **Deliverable**: All .py files have type hints. `mypy .` passes with no errors.
- **Acceptance criteria**: Run `mypy shared/ fundamentals/ projects/ --strict` and fix all errors
- **Estimated time**: 5 hours
- **Come back for review**: Yes (review in batches)

### 2.3 Implement Strategy pattern in a project
- [ ] **Status: Not Started**
- **What to do**: Refactor one of the projects to use Strategy pattern (e.g., different data validation strategies, or different aggregation strategies).
- **What to learn**: Strategy pattern (define family of algorithms, make them interchangeable). When to use it. How it relates to dependency injection.
- **Research**: Design Patterns book. Python-specific strategy pattern examples.
- **Deliverable**: At least one project using Strategy pattern with documentation
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 2.4 Implement Factory pattern
- [ ] **Status: Not Started**
- **What to do**: Create a factory for SparkSession configurations (dev, test, prod configs) or for data source readers (CSV, Parquet, JSON).
- **What to learn**: Factory pattern (object creation logic). Why factories make code more testable and flexible.
- **Deliverable**: Factory implementation in `shared/` or in a project
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 2.5 Add pre-commit hooks
- [ ] **Status: Not Started**
- **What to do**: Create `.pre-commit-config.yaml` with ruff for linting and formatting. Install pre-commit hooks.
- **What to learn**: Git hooks. Code quality automation. Why linting before commit catches issues early. Ruff (fast Python linter/formatter).
- **Research**: pre-commit documentation. ruff documentation.
- **Deliverable**: `.pre-commit-config.yaml` at repo root. Hooks installed and working.
- **Acceptance criteria**: Run `git commit` on poorly formatted code and see it auto-fixed
- **Estimated time**: 1 hour
- **Come back for review**: Yes

### 2.6 Refactor duplicated code
- [ ] **Status: Not Started**
- **What to do**: Find duplicated logic across projects and extract into shared utilities. Examples: camel_to_snake (appears in 2 files with bugs), common data validation patterns.
- **What to learn**: DRY principle application. When to abstract vs when to keep separate. Code smell recognition.
- **Research**: Use a code duplication detector or manual review
- **Deliverable**: New shared utility modules. Updated projects using them.
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 2.7 Add pytest to all projects
- [ ] **Status: Not Started**
- **What to do**: Add comprehensive pytest tests for each portfolio project. Test data processing logic, transformations, edge cases.
- **What to learn**: Testing PySpark code. Mocking external dependencies. Integration tests vs unit tests. Pytest fixtures for SparkSession.
- **Research**: How to test PySpark applications. Shared SparkSession fixtures.
- **Deliverable**: `projects/*/tests/` directories with good coverage
- **Estimated time**: 6 hours
- **Come back for review**: Yes (review per project)

### 2.8 Build a CLI data profiler project
- [ ] **Status: Not Started**
- **What to do**: Create a small CLI tool that profiles CSV/Parquet files (row count, null rates, data types, cardinality, sample values). Use argparse or click.
- **What to learn**: CLI application design. Argument parsing. Data profiling patterns. Pretty-printing tabular output.
- **Research**: argparse or click documentation. pandas describe() and info() for inspiration.
- **Deliverable**: `fundamentals/python/projects/data_profiler/` with CLI tool and tests
- **Estimated time**: 4 hours
- **Come back for review**: Yes

### 2.9 Add comprehensive docstrings
- [ ] **Status: Not Started**
- **What to do**: Add Google-style or NumPy-style docstrings to all public functions and classes.
- **What to learn**: Docstring conventions. What makes good documentation. Sphinx-compatible formats.
- **Research**: PEP 257. Google Python Style Guide.
- **Deliverable**: All shared modules and projects have docstrings
- **Estimated time**: 3 hours
- **Come back for review**: No

### 2.10 Create Makefile for common commands
- [ ] **Status: Not Started**
- **What to do**: Create a Makefile with targets: install, test, lint, format, clean, type-check
- **What to learn**: Makefiles for task automation. Why developers use make even for non-compiled languages. Phony targets.
- **Research**: Makefile basics. Look at other Python project Makefiles.
- **Deliverable**: `Makefile` at repo root with documented targets
- **Acceptance criteria**: `make test`, `make lint`, `make format` all work correctly
- **Estimated time**: 1.5 hours
- **Come back for review**: Yes

---

## Total Estimated Time: ~32 hours
Focus on building production-grade Python habits that will serve you in any role.
