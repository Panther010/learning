# Phase 5: Orchestration, dbt, and Data Quality

**Target**: Weeks 25-30 | ~36 hours total | 5-7 hrs/week

<!--
AMENDABLE: Add, remove, or reorder tasks freely.
This phase adds production operations to the ecommerce pipeline from Phase 4.
-->

## Goals
- Airflow for pipeline orchestration
- dbt for SQL transformation layer
- Great Expectations for data quality
- Learn how production data platforms are operated

## Tasks

### 5.1 Local Airflow setup with Docker
- [ ] **Status: Not Started**
- **What to do**: Add Airflow to the ecommerce pipeline's docker-compose.yml. Get the web UI running at localhost:8080.
- **What to learn**: Airflow architecture (webserver, scheduler, worker, metadata DB). Executor types (SequentialExecutor for local dev). DAG bag and how Airflow discovers DAGs.
- **Research**: Airflow docs "Running Airflow in Docker". Use the official docker-compose provided by Apache Airflow as a starting point.
- **Deliverable**: Airflow running in Docker with web UI accessible.
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 5.2 First DAG: simple file processing
- [ ] **Status: Not Started**
- **What to do**: Write a DAG that watches for new files in a directory, triggers a Spark job. Start simple before orchestrating the full pipeline.
- **What to learn**: DAG authoring. Operators (BashOperator, PythonOperator). Task dependencies (`>>` operator). Scheduling (cron expressions). Sensors (FileSensor).
- **Deliverable**: `dags/file_processing_dag.py`
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 5.3 Ecommerce pipeline DAG
- [ ] **Status: Not Started**
- **What to do**: Orchestrate the full ecommerce pipeline: bronze -> silver -> gold with proper task dependencies.
- **What to learn**: XCom for passing data between tasks. Task retries and failure handling. DAG scheduling and backfilling. Airflow connections for external systems.
- **Deliverable**: `dags/ecommerce_pipeline_dag.py`
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 5.4 Custom Airflow operator
- [ ] **Status: Not Started**
- **What to do**: Create a custom operator (e.g., DeltaTableSensor that waits for a Delta table to have new data, or a SparkJobOperator that submits and monitors a Spark job).
- **What to learn**: Custom operator development. Operator templating. Airflow plugin system.
- **Deliverable**: `plugins/operators/` with at least one custom operator used in your DAG.
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 5.5 dbt project setup
- [ ] **Status: Not Started**
- **What to do**: Initialize a dbt project for gold layer SQL transformations. Connect to a local PostgreSQL or DuckDB for the SQL layer.
- **What to learn**: dbt project structure (`dbt_project.yml`, `profiles.yml`). Sources, models, seeds. Why dbt became the standard for analytics transformation.
- **Research**: dbt docs "Getting Started" tutorial. Understand the difference between dbt and Spark (dbt is SQL-first, Spark is code-first).
- **Deliverable**: `projects/ecommerce_pipeline/dbt/` with initialized dbt project.
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 5.6 dbt models for gold layer
- [ ] **Status: Not Started**
- **What to do**: Implement 3-5 dbt models: revenue summary, conversion funnel, customer segments, top products.
- **What to learn**: `ref()` and `source()` functions. Model materialization (view, table, incremental). Jinja templating in SQL. dbt's DAG and dependency resolution.
- **Deliverable**: 3-5 models in `dbt/models/` that build gold-layer tables.
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 5.7 dbt tests and documentation
- [ ] **Status: Not Started**
- **What to do**: Add schema tests (not_null, unique, accepted_values, relationships) and generate dbt docs.
- **What to learn**: dbt testing philosophy. Schema.yml. Custom test macros. `dbt docs generate` + `dbt docs serve`.
- **Deliverable**: `schema.yml` with tests. Generated documentation site.
- **Estimated time**: 1.5 hours
- **Come back for review**: Yes

### 5.8 Great Expectations integration
- [ ] **Status: Not Started**
- **What to do**: Add data quality validation between pipeline stages using Great Expectations (or a simpler alternative if GE feels too heavy).
- **What to learn**: Expectation suites. Data validation patterns. Data docs. How quality gates prevent bad data from reaching consumers.
- **Deliverable**: Quality suite validating bronze->silver transition.
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 5.9 DAG testing
- [ ] **Status: Not Started**
- **What to do**: Write pytest tests for DAG validity — verify imports, task dependencies, no cycles.
- **What to learn**: Testing Airflow DAGs. DAG bag loading. Why DAG import tests catch common errors before deployment.
- **Deliverable**: `tests/test_dags.py`
- **Estimated time**: 1 hour
- **Come back for review**: Yes

### 5.10 Alerting and SLA monitoring
- [ ] **Status: Not Started**
- **What to do**: Add failure callbacks (Slack/email notification on DAG failure). Add SLA definitions.
- **What to learn**: Airflow callbacks (`on_failure_callback`). SLA misses. Monitoring patterns for data pipelines.
- **Deliverable**: Enhanced DAGs with failure callbacks and SLA monitoring.
- **Estimated time**: 1.5 hours
- **Come back for review**: Yes

---

## Total Estimated Time: ~20.5 hours
Orchestration and data quality are critical for production data platforms.
