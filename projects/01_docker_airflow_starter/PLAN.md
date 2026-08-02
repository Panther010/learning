# Olympic Medallion Architecture — Project Plan

## Goal
Build a Bronze/Silver/Gold (medallion architecture) data pipeline on the Olympic Games
dataset, orchestrated with **Airflow**, containerized with **Docker**, processed with
**PySpark**. Secondary goal: learn Docker and Airflow from near-zero, one phase at a time,
without letting orchestration complexity swamp the data engineering learning.

## Dataset
4 source CSVs: `olympic_athletes.csv`, `olympic_hosts.csv`, `olympic_medals.csv`,
`olympic_results.csv`. Path: /Users/bakulseth/PycharmProjects/learning/data/raw/olympic/2022
~21k medals, ~162k results, ~74k athletes, 53 hosts.
Known issues to handle: broken rows in athletes (unescaped bio field), stringified
list column in results (`athletes`), string-typed numeric columns, inconsistent
country naming across eras (Soviet Union / Russian Federation / ROC).

## Guiding Principles
- One phase at a time. Do not start Phase N+1 until Phase N's checkpoint passes.
- Docker learning and Airflow learning are deliberately separated (Phase 1 vs Phase 2)
  so failures are easier to diagnose.
- Every Spark script should be runnable **standalone** (outside Airflow) for
  debugging, before being wired into a DAG.
- Every generated file (by Claude Code / Codex / any AI agent) must be reviewed by
  the project owner before running. See AGENT.md for review protocol.

## Directory Structure

```
projects/01_docker_airflow_starter/
├── docker-compose.yaml
├── .env
├── dags/
│   ├── bronze_ingest_dag.py
│   ├── silver_transform_dag.py
│   └── gold_aggregate_dag.py
├── spark_jobs/
│   ├── Dockerfile
│   ├── bronze/
│   │   └── ingest_raw.py
│   ├── silver/
│   │   ├── clean_athletes.py
│   │   ├── clean_medals.py
│   │   ├── clean_results.py
│   │   └── clean_hosts.py
│   └── gold/
│       ├── dim_country.py
│       ├── dim_athlete.py
│       ├── dim_host.py
│       ├── fact_medals.py
│       └── country_medal_summary.py
├── tests/
│   ├── test_silver_transforms.py
│   └── test_data_quality.py
├── logs/
├── plugins/
├── requirements.txt
└── README.md
```

---

## Phase 0 — Mental Model (no files created)
Understand before coding:
- **Docker**: packages an environment (OS + software + config) into an image;
  a container is a running instance of an image. Docker Compose runs multiple
  containers together.
- **Airflow**: an orchestrator. You write DAGs (Python files) describing tasks
  and dependencies. Airflow triggers work; it doesn't do the heavy lifting itself.
- **Fit together**: Airflow triggers a Spark job (via BashOperator/SparkSubmitOperator/
  DockerOperator) → Spark job reads/writes Bronze/Silver/Gold parquet on a shared
  volume mounted into whichever container runs it.

**Checkpoint:** Can explain image vs container, and DAG vs task, in your own words.

---

## Phase 1 — Docker Basics (Spark only, no Airflow) — Complete
**Objective:** get comfortable with Docker in isolation.

Steps:
1. Install Docker Desktop.
2. Write a minimal `spark_jobs/Dockerfile` — Python + PySpark, nothing else.
3. `docker build` it, `docker run` it with a volume mount (`-v`) pointing at `data/`.
4. Run one existing script inside the container manually.

**Checkpoint:** Explain what an image vs a container is, what `-v` does, and why
you need it (persistence after the container stops).

**Files created:** `spark_jobs/Dockerfile`

**Checkpoint passed:** Docker image built and the Python, Java, and PySpark runtime
were verified by the project owner. The verification container was stopped after use.

---

## Phase 2 — Bronze Spark Development (standalone)
**Objective:** build and verify raw ingestion without Docker Compose or Airflow.

Steps:
1. Write `spark_jobs/bronze/ingest_raw.py`:
   - read all 4 CSVs with explicit all-StringType schemas, `multiLine=True`, and
     `escape='"'`; preserve parser-level malformed rows in `_corrupt_record`
   - add `_ingested_at`, `_source_file` metadata columns
   - write to `data/processed/olympic_2022/bronze/<table_name>/` as Parquet
   - do NOT drop bad rows at this layer
2. Run it first on the host with `spark-submit`, then inside the Phase 1 Docker image
   with `data/` mounted at `/opt/data`.
3. Compare row counts and schemas between source CSVs and Bronze Parquet output.

**Checkpoint:** The script completes both locally and in Docker; the four Bronze
Parquet datasets exist under `data/processed/olympic_2022/bronze/`, and documented
row counts match the raw input.

**Files created:** `spark_jobs/bronze/ingest_raw.py`, `spark_jobs/utils/spark_session.py`

---

## Phase 3 — Silver Spark Development (standalone)
**Objective:** build data-cleaning jobs and validate their outputs before orchestration.

Steps:
1. Write `spark_jobs/silver/clean_athletes.py`:
   - quarantine corrupted rows to `data/processed/olympic_2022/silver/_rejects/olympic_athletes/`
   - dedupe on `athlete_url` via window function, keep most complete row
2. Write `clean_hosts.py`, `clean_medals.py`, `clean_results.py`:
   - cast numeric/date types (`games_participations`, `athlete_year_birth`,
     `rank_position` → int, capturing DNS/DNF/DQ into `rank_status`)
   - parse the stringified `athletes` array column in results into a real
     array-of-structs
   - standardise `game_slug` from hosts to `slug_game`, then validate `slug_game`
     values from medals/results against hosts with an anti-join check
3. Run each script with `spark-submit` against Bronze output; add pytest tests for
   the transformation functions before adding any Airflow DAGs.

**Checkpoint:** All four Silver scripts run standalone, write expected output and
reject records, and their tests pass.

**Files created:** 4 files under `spark_jobs/silver/`, `tests/test_silver_transforms.py`,
`tests/test_data_quality.py`

---

## Phase 4 — Gold Spark Development (standalone)
**Objective:** build the star schema and one useful analysis from validated Silver data.

Steps:
1. Build dimensions:
   - `dim_country.py` — union distinct country fields from medals + results,
     resolve naming inconsistencies (see "Country Identity" note below)
   - `dim_athlete.py`, `dim_host.py`
2. Build facts:
   - `fact_medals.py` — medal-grain fact table + a bridge table
     `bridge_medal_athlete` for team medals (don't explode team medals into the
     fact table itself — that changes the grain)
3. Build summary/pivot tables (pick from the problem list below), e.g.
   `country_medal_summary.py`.
4. Run each job with `spark-submit`; validate table grain, keys, and row counts
   before writing Parquet.

**Checkpoint:** Dimension, fact, bridge, and selected summary outputs exist in Gold;
their documented data contracts and tests pass.

**Files created:** 5+ files under `spark_jobs/gold/`

### Country Identity Note (design decision required)
Decide and document: is "Soviet Union" → "Russian Federation" → "ROC" one
historical entity (SCD Type 2 with `valid_from`/`valid_to`) or three separate
rows conformed to a "current name" mapping? Either is defensible — document
the choice in `dim_country.py` as a comment and in the README.

---

## Phase 5 — Airflow Orchestration (after standalone Spark verification)
**Objective:** learn Airflow and orchestrate the already-tested Spark jobs.

Steps:
1. Adapt Apache Airflow's official reference `docker-compose.yaml`; use its
   PostgreSQL service as Airflow's metadata database. Pin all image and Python
   dependency versions.
2. Start the stock environment with `docker compose up airflow-init`, then
   `docker compose up`; explore the UI and trigger an example DAG.
3. Extend Compose with a Spark standalone master and one worker. Mount `data/` and
   `spark_jobs/` into Spark and Airflow at documented, consistent container paths.
4. Configure Airflow with a Spark connection and create three DAGs:
   `bronze_ingest_dag`, `silver_transform_dag`, and `gold_aggregate_dag`.
5. Each DAG uses the same teaching sequence: `PythonOperator` preflight check →
   `SparkSubmitOperator` job(s) → `BashOperator` output verification. Model Bronze
   as one job, Silver as parallel jobs, and Gold as dimension/fact fan-in.

**Checkpoint:** A manual Bronze → Silver → Gold run succeeds from the Airflow UI,
and the Graph view accurately represents the dependency shapes.

**Files created:** `docker-compose.yaml`, `.env.example`, `requirements.txt`, and
three DAG files under `dags/`.

---

## Phase 6 — Orchestration Polish
Steps:
1. Add a `schedule_interval` (arbitrary, e.g. `@daily`, or `None` for manual-only
   since this is historical data — document the choice).
2. Add explicit data-quality-check tasks (not just asserts buried in Spark code)
   that fail the DAG on unexpected row-count drops or null-rate spikes.
3. Replace hardcoded paths with Airflow Variables/Connections.
4. Add retries, `on_failure_callback` stub, and note where a real Slack/email
   alert would plug in.

**Checkpoint:** A DAG failure produces a clear, actionable Airflow UI alert.

---

## Phase 7 — Wrap-up
Steps:
1. Write `README.md`: architecture description, how to run (`docker-compose up`),
   an architecture diagram.
2. Expand and document the pytest suite for Silver/Gold DataFrames (row counts,
   null rates, schema conformance).
3. Optional stretch: a small Streamlit dashboard reading Gold parquet.

---

## Gold-Layer Practice Problems (pick as many as useful; not all required)
1. Medal table pivot: rows = country, columns = medal_type, values = count, for one Games.
2. Trend pivot: rows = country, columns = game_year, values = total medals (requires join first).
3. Discipline popularity pivot: rows = discipline, columns = season, values = event count.
4. Gender participation pivot: rows = discipline, columns = event_gender, values = medal count.
5. Multi-metric pivot: medal count vs distinct medalist count per country per medal_type.
6. Athlete career leaderboard: pivot medal_type per athlete, rank by total.
7. Host country advantage: pivot is_host_country (True/False) vs medal_type, compare averages.

## Data-Modeling / Cleaning Practice Problems
1. Quantify corrupted-row rate in bronze `olympic_athletes`.
2. Test whether `multiLine`/`escape` CSV options fix the broken bio-field rows.
3. Cast `rank_position` with `rank_status` fallback for DNS/DNF/DQ.
4. Parse `athletes` stringified list into array-of-structs; explode to one row
   per athlete per team-result.
5. Anti-join `slug_game` across medals/results vs hosts — find orphans.
6. Check `country_code` ↔ `country_3_letter_code` consistency across rows.
7. Dedupe athletes on `athlete_url`, keep most-complete row via window function.
8. Build `dim_country` with an explicit, documented conforming rule.
9. Design `fact_medals` at true medal-grain with a separate bridge table for team medals.
10. Write a data contract (grain, PK, non-null expectations) per Gold table and an
    assertion function that validates before writing.

## Status Tracking
Update this section as phases complete:

- [ ] Phase 0 — Mental model
- [x] Phase 1 — Docker basics
- [ ] Phase 2 — Bronze Spark development
- [ ] Phase 3 — Silver Spark development
- [ ] Phase 4 — Gold Spark development
- [ ] Phase 5 — Airflow orchestration
- [ ] Phase 6 — Orchestration polish
- [ ] Phase 7 — Wrap-up
