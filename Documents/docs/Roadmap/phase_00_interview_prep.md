# Phase 0: Interview Preparation (Weeks 1-4)

**Priority:** URGENT - Resigning this week, interviews likely in 2-3 weeks
**Time commitment:** 7-8 hours/day
**Goal:** Be interview-ready while building portfolio projects that demonstrate AI + Modern DE skills
**Status:** Not Started

---

## Overview

This is a NEW phase inserted BEFORE Phase 1. It front-loads urgent interview prep while simultaneously making progress on the learning repo. You'll build 4 portfolio projects that are BOTH interview talking points AND contributions to the learning repo structure.

**Key principle:** Everything you study gets committed to the learning repo, creating a portfolio as you prep.

---

## Daily Routine (7-8 hours)

### Morning — Core Skills Sharpening (3 hours)

| Hour | Focus | Repo Integration |
|------|-------|------------------|
| 1 | **SQL Practice** — 2 hard problems (window functions, CTEs, recursive, pivots) | Add to `fundamentals/sql/interview_prep/` with detailed comments explaining the approach |
| 2 | **PySpark Coding** — 1 transformation from scratch (no lookup) | Add to `fundamentals/spark/interview_prep/` — test your muscle memory |
| 3 | **Python DSA + Core** — 1 medium LeetCode + daily concept (decorators, generators, collections, etc.) | Add to `fundamentals/python/interview_prep/` with complexity analysis |

### Afternoon — Concepts & System Design (2.5 hours)

| Hour | Focus | Repo Integration |
|------|-------|------------------|
| 4 | **AWS Deep Revision** (W1-2) or **System Design Practice** (W3-4) | Create `docs/notes/aws_cheatsheet.md` and `docs/notes/system_design_patterns.md` |
| 5 | **Concept of the Day** — Rotate: partitioning, Delta vs Parquet, Spark internals, data modelling, SCDs, exactly-once, backfill strategies | Add to `docs/notes/concepts/` — one markdown file per concept |
| 5.5 | **AI Theory** (30 min) — See AI learning schedule below | Add to `docs/notes/ai/` — summarize in your own words |

### Evening — Portfolio Projects (2.5 hours)

| Week | Gap-Filling Project | AI Project | Where it goes in repo |
|------|---------------------|------------|----------------------|
| 1 | Docker + Airflow basics | Claude API basics | `projects/01_docker_airflow_starter/` |
| 2 | Delta Lake + pytest | SQL Generator Tool | `projects/02_sql_generator_ai/` |
| 3 | dbt basics | RAG Pipeline | `projects/03_dbt_fundamentals/` + `projects/04_rag_doc_search/` |
| 4 | Spark Streaming | Data Quality AI Assistant | `projects/05_streaming_pipeline/` + `projects/06_dq_ai_assistant/` |

### Daily Non-Negotiables (30 min)

- [ ] Apply to 5-10 jobs (LinkedIn Easy Apply + direct)
- [ ] Update LinkedIn or resume based on what you learned today
- [ ] Git commit your daily work with descriptive messages

---

## Week 1: Docker + Airflow + Claude API

### Morning Drills (Week 1 Tracker)

**SQL:**
- [ ] Mon: Hard window function problem
- [ ] Tue: Hard recursive CTE problem
- [ ] Wed: Hard pivot/unpivot problem
- [ ] Thu: Hard self-join problem
- [ ] Fri: Hard date/time manipulation problem
- [ ] Sat-Sun: 4 more hard problems (10 total for the week)

**PySpark:**
- [ ] Mon: Complex aggregation with multiple groupBy levels
- [ ] Tue: Window function with custom partitioning
- [ ] Wed: Multiple join types with broadcast
- [ ] Thu: UDF with complex logic + type hints
- [ ] Fri: Repartition + coalesce optimization exercise

**Python:**
- [ ] Mon: Medium LeetCode + learn decorators (@property, @classmethod, @staticmethod, custom)
- [ ] Tue: Medium LeetCode + learn generators (yield, generator expressions, itertools)
- [ ] Wed: Medium LeetCode + learn collections (Counter, defaultdict, deque, namedtuple)
- [ ] Thu: Medium LeetCode + learn context managers (with statement, contextlib)
- [ ] Fri: Medium LeetCode + learn exception handling (custom exceptions, try/except/else/finally)

### Afternoon Study (Week 1 Tracker)

**AWS Deep Dive:**
- [ ] Mon: S3 (buckets, versioning, lifecycle, encryption, access patterns) + Glue (catalog, crawlers, ETL jobs)
- [ ] Tue: EMR (cluster modes, instance types, step functions) + Redshift (architecture, distribution keys, sort keys)
- [ ] Wed: Lambda (triggers, layers, cold starts) + Athena (partitioning, query optimization, federated queries)
- [ ] Thu: Step Functions (state machines, error handling) + EventBridge (event patterns, rules)
- [ ] Fri: IAM (roles, policies, least privilege) + CloudWatch (logs, metrics, alarms)

**Concepts:**
- [ ] Mon: Partitioning strategies (hash, range, list) — when to use each
- [ ] Tue: Delta Lake vs Parquet — ACID, time travel, optimization
- [ ] Wed: Spark internals — Catalyst optimizer, Tungsten execution, shuffle mechanics
- [ ] Thu: Data modelling — star schema, snowflake, data vault, dimensional modelling
- [ ] Fri: Slowly Changing Dimensions — Type 1, 2, 3 with PySpark examples

**AI Theory (30 min/day):**
- [ ] Mon: Prompt engineering patterns — few-shot, chain-of-thought, role prompting, system prompts
- [ ] Tue: RAG fundamentals — vector embeddings, chunking strategies, retrieval vs generation
- [ ] Wed: LLM basics — tokens, context windows, temperature, top-p, stop sequences
- [ ] Thu: AI in data engineering — SQL generation, schema inference, data quality checks, documentation
- [ ] Fri: AI tools landscape — Claude API, OpenAI API, LangChain, LlamaIndex, ChromaDB, Pinecone

### Evening Projects (Week 1)

#### Project 1: Docker + Airflow Starter (`projects/01_docker_airflow_starter/`)

**Goal:** Containerized PySpark job orchestrated by Airflow

**Tasks:**
- [ ] Create project structure:
  ```
  projects/01_docker_airflow_starter/
  ├── README.md
  ├── docker-compose.yml
  ├── Dockerfile.spark
  ├── airflow/
  │   └── dags/
  │       └── spark_job_dag.py
  ├── spark_jobs/
  │   └── sample_etl.py
  ├── data/
  │   └── input/
  └── config.yaml
  ```
- [ ] Write Dockerfile for PySpark environment
- [ ] Write docker-compose.yml (Spark standalone + Postgres)
- [ ] Create a simple PySpark ETL job (read CSV → transform → write Parquet)
- [ ] Install Airflow using Astro CLI or docker-compose
- [ ] Write Airflow DAG with: PythonOperator → SparkSubmitOperator → BashOperator
- [ ] Add retries, email alerting (mock), and task dependencies
- [ ] Document setup instructions in README.md
- [ ] Test end-to-end: `docker-compose up` → trigger DAG → verify output

**Interview talking points:** "I containerized a PySpark pipeline and orchestrated it with Airflow, including retry logic and dependency management"

#### Project 2: Claude API Basics (`projects/02_sql_generator_ai/` - partial, finish in Week 2)

**Goal:** Python CLI tool that generates SQL from natural language

**Week 1 tasks:**
- [ ] Get Claude API key from console.anthropic.com
- [ ] Install `anthropic` Python SDK: `pip install anthropic`
- [ ] Write `api_basics.py`: Send prompt → get response
- [ ] Experiment with system prompts for SQL generation
- [ ] Implement prompt caching for table schemas
- [ ] Test structured output (JSON mode) for SQL + explanation

---

## Week 2: Delta Lake + pytest + SQL Generator AI

### Morning Drills (Week 2 Tracker)

**SQL:**
- [ ] 10 more hard problems (focus: correlated subqueries, EXISTS/NOT EXISTS, complex HAVING)
- Total so far: 20 problems

**PySpark:**
- [ ] 5 more transformation exercises (focus: DataFrame API vs SQL, explode/collect_list, struct handling)
- Total so far: 10 exercises

**Python:**
- [ ] 5 medium LeetCode problems
- [ ] Daily concepts: Mon=async/await basics, Tue=dataclasses, Wed=typing (Protocol, TypeVar), Thu=functools (lru_cache, partial), Fri=pathlib
- Total LeetCode: 10 problems

### Afternoon Study (Week 2 Tracker)

**AWS (continued) or System Design:**
- [ ] Mon-Tue: Finish AWS services (DynamoDB, Kinesis, SQS, SNS)
- [ ] Wed-Fri: System design practice — Design a data lake architecture (draw diagrams, explain trade-offs)

**Concepts:**
- [ ] Mon: Exactly-once semantics in streaming
- [ ] Tue: Backfill strategies (full reload, incremental, lookback window)
- [ ] Wed: Data quality dimensions (completeness, accuracy, consistency, timeliness)
- [ ] Thu: Idempotency in data pipelines
- [ ] Fri: Change Data Capture (CDC) patterns

**AI Theory:**
- [ ] Mon: Vector databases — embeddings, cosine similarity, approximate nearest neighbor
- [ ] Tue: MCP architecture — servers, tools, resources, how Claude Code uses it
- [ ] Wed: AI agents — tool use, multi-step reasoning, ReAct pattern
- [ ] Thu: Responsible AI — hallucination mitigation, grounding, evaluation
- [ ] Fri: Cost & architecture — token pricing, caching strategies, model selection (Haiku vs Sonnet vs Opus)

### Evening Projects (Week 2)

#### Project 1: Delta Lake + pytest (`fundamentals/spark/delta_lake/`)

**Tasks:**
- [ ] Convert one of your existing PySpark projects to use Delta format
- [ ] Implement MERGE for upserts (slowly changing dimension Type 2)
- [ ] Use time travel to query historical versions
- [ ] Test Z-ordering for query optimization
- [ ] Write pytest tests for transformations using chispa:
  ```python
  # test_transformations.py
  from chispa.dataframe_comparer import assert_df_equality
  
  def test_customer_aggregation(spark):
      input_df = ...
      result_df = aggregate_customers(input_df)
      expected_df = ...
      assert_df_equality(result_df, expected_df)
  ```
- [ ] Create conftest.py with SparkSession fixture
- [ ] Run tests: `pytest fundamentals/spark/delta_lake/tests/`

**Interview talking point:** "I use Delta Lake for ACID transactions and implement pytest with chispa for PySpark test coverage"

#### Project 2: SQL Generator AI Tool (finish from Week 1)

**Tasks:**
- [ ] Create project structure:
  ```
  projects/02_sql_generator_ai/
  ├── README.md
  ├── sql_generator/
  │   ├── __init__.py
  │   ├── cli.py
  │   ├── schema_parser.py
  │   ├── prompt_builder.py
  │   └── claude_client.py
  ├── tests/
  │   └── test_sql_generator.py
  ├── examples/
  │   ├── ecommerce_schema.sql
  │   └── sample_questions.txt
  └── config.yaml
  ```
- [ ] Implement schema parser (read DDL or DESCRIBE TABLE output)
- [ ] Build prompt: system prompt + schema + user question → SQL
- [ ] Call Claude API with structured output (JSON with sql and explanation fields)
- [ ] Add CLI with click: `python -m sql_generator.cli --schema schema.sql --question "top 10 customers"`
- [ ] Test against 10 known questions from your SQL fundamentals
- [ ] Write unit tests with pytest
- [ ] Document usage in README

**Interview talking point:** "I built an AI-powered SQL generator using Claude API with prompt engineering and structured outputs"

---

## Week 3: dbt + RAG Pipeline

### Morning Drills (Week 3 Tracker)

**SQL:**
- [ ] 10 more hard problems (focus: optimization, query plans, index usage)
- Total so far: 30 problems

**PySpark:**
- [ ] 5 more exercises (focus: custom accumulators, broadcast variables, performance tuning)
- Total so far: 15 exercises

**Python:**
- [ ] 5 medium LeetCode (focus: graphs, trees, dynamic programming)
- Total so far: 15 problems

### Afternoon Study (Week 3 Tracker)

**System Design:**
- [ ] Mon: Design a real-time fraud detection pipeline (Kafka → Spark Streaming → Delta → alerting)
- [ ] Tue: Design a CDC system (database → Debezium → Kafka → sink)
- [ ] Wed: Design a data warehouse migration (on-prem → cloud, schema mapping, data validation)
- [ ] Thu: Design a medallion architecture (bronze/silver/gold layers, incremental processing)
- [ ] Fri: Design a multi-tenant data platform (isolation, security, cost allocation)

**Concepts:**
- [ ] Mon: Broadcast joins vs shuffle joins
- [ ] Tue: Spark adaptive query execution (AQE)
- [ ] Wed: Checkpointing in Spark Streaming
- [ ] Thu: Watermarks in structured streaming
- [ ] Fri: Event time vs processing time

**AI Theory:**
- Practice explaining AI concepts from Weeks 1-2 out loud (mock interview format)

### Evening Projects (Week 3)

#### Project 1: dbt Fundamentals (`projects/03_dbt_fundamentals/`)

**Tasks:**
- [ ] Complete dbt fundamentals course (free, ~4 hours total): courses.getdbt.com
- [ ] Install dbt-core with DuckDB adapter: `pip install dbt-core dbt-duckdb`
- [ ] Initialize dbt project: `dbt init dbt_fundamentals`
- [ ] Load sample data into DuckDB (use one of your existing datasets)
- [ ] Build dbt models:
  - `models/staging/stg_customers.sql` — basic SELECT with renaming
  - `models/marts/fct_orders.sql` — join customers + orders
  - `models/marts/dim_customers.sql` — customer dimension with aggregates
- [ ] Add dbt tests (unique, not_null, relationships, accepted_values)
- [ ] Write a custom dbt test (e.g., check that total_amount > 0)
- [ ] Run: `dbt run`, `dbt test`, `dbt docs generate`
- [ ] Document lineage and tests

**Interview talking point:** "I use dbt for SQL transformation layers with built-in testing and data lineage"

#### Project 2: RAG Pipeline (`projects/04_rag_doc_search/`)

**Goal:** Query your DQ/DG documentation using RAG

**Tasks:**
- [ ] Install ChromaDB: `pip install chromadb`
- [ ] Create project structure:
  ```
  projects/04_rag_doc_search/
  ├── README.md
  ├── rag_pipeline/
  │   ├── __init__.py
  │   ├── document_loader.py
  │   ├── chunker.py
  │   ├── embedder.py
  │   ├── retriever.py
  │   └── query_engine.py
  ├── docs_corpus/
  │   └── (copy your DQ/DG markdown docs here)
  ├── tests/
  └── cli.py
  ```
- [ ] Load markdown documents from docs_corpus/
- [ ] Chunk documents (500-1000 tokens per chunk with overlap)
- [ ] Generate embeddings using Claude API or sentence-transformers
- [ ] Store in ChromaDB vector database
- [ ] Implement retrieval: query → top-k similar chunks
- [ ] Send chunks + query to Claude API for final answer
- [ ] Build CLI: `python cli.py "How do I configure DQ for large datasets?"`
- [ ] Test with 10 questions about DQ/DG tools
- [ ] Document the RAG pipeline architecture

**Interview talking point:** "I built a RAG pipeline with vector embeddings and ChromaDB to enable semantic search over technical documentation"

---

## Week 4: Streaming + Data Quality AI Assistant

### Morning Drills (Week 4 Tracker)

**SQL:**
- [ ] 10 more hard problems
- Total: 40 problems ✅

**PySpark:**
- [ ] 5 more exercises (focus: structured streaming basics)
- Total: 20 exercises ✅

**Python:**
- [ ] 5 medium LeetCode
- Total: 20 problems ✅

### Afternoon Study (Week 4 Tracker)

**System Design:**
- Continue practicing designs from Week 3, but now add: cost estimation, failure modes, monitoring strategy

**Concepts:**
- Review all concepts from Weeks 1-3. Create a cheat sheet.

**AI Theory:**
- Mock interview practice: Explain RAG, prompt engineering, vector databases, AI in DE pipelines

### Evening Projects (Week 4)

#### Project 1: Spark Streaming Pipeline (`projects/05_streaming_pipeline/`)

**Goal:** Kafka → Spark Structured Streaming → Delta Lake

**Tasks:**
- [ ] Set up Kafka locally using Docker: `docker-compose.yml` with Kafka + Zookeeper
- [ ] Create Kafka topic: `streaming_events`
- [ ] Write Python producer: generate mock events (e.g., user actions, sensor data)
- [ ] Write Spark Structured Streaming consumer:
  - Read from Kafka topic
  - Parse JSON events
  - Apply transformations (filter, aggregate by window)
  - Write to Delta Lake sink
- [ ] Implement watermark for late data handling
- [ ] Set up checkpointing
- [ ] Test: produce events → verify they appear in Delta table
- [ ] Document architecture and data flow

**Interview talking point:** "I built a real-time streaming pipeline with Kafka and Spark Structured Streaming, writing to Delta Lake with watermarking and checkpointing"

#### Project 2: Data Quality AI Assistant (`projects/06_dq_ai_assistant/`)

**Goal:** AI-powered data quality analysis tool

**Tasks:**
- [ ] Create CLI tool that:
  1. Reads a CSV/Parquet file
  2. Profiles it (row count, null %, data types, basic stats, unique values)
  3. Sends profile to Claude API
  4. Gets back: quality issues, anomalies, recommendations
- [ ] Project structure:
  ```
  projects/06_dq_ai_assistant/
  ├── README.md
  ├── dq_assistant/
  │   ├── __init__.py
  │   ├── profiler.py        # Data profiling logic
  │   ├── claude_analyzer.py # Claude API integration
  │   ├── report_generator.py
  │   └── cli.py
  ├── tests/
  ├── sample_data/
  └── output/
  ```
- [ ] Implement profiler using pandas or PySpark
- [ ] Design prompt: send profile → ask Claude to identify quality issues
- [ ] Parse Claude response into structured recommendations
- [ ] Generate markdown report with findings
- [ ] Test on 3 datasets with known quality issues
- [ ] Add CLI: `python -m dq_assistant.cli --file data.csv --output report.md`

**Interview talking point:** "I combined my data quality expertise with LLMs to build an AI assistant that analyzes datasets and provides actionable quality recommendations"

---

## Integration with Original Learning Plan

**After Week 4 (Phase 0 completion):**

You'll have:
- ✅ 40 hard SQL problems done
- ✅ 20 PySpark exercises done
- ✅ 20 Python LeetCode problems done
- ✅ 6 portfolio projects built and committed
- ✅ Interview stories ready
- ✅ Resume updated with AI/LLM skills

**Then you continue to Phase 1-6:**

- **Phase 1 (Foundation):** You've already created shared modules during Phase 0 projects. Skip tasks 1.6-1.9, go straight to restructuring.
- **Phase 2 (Python Engineering):** Add pytest, type hints, pre-commit hooks to your 6 new projects.
- **Phase 3 (Spark Depth):** Deepen streaming, Delta Lake, optimization from Phase 0 basics.
- **Phase 4 (End-to-End Project):** Build the ecommerce pipeline as planned.
- **Phase 5 (Orchestration):** Deepen Airflow, add dbt, Great Expectations.
- **Phase 6 (Cloud AWS):** Terraform, Glue, Athena as planned.

---

## Resume Updates After Each Week

### After Week 1:
- Add: Docker, Airflow, Claude API
- Update summary to remove "aspiring to" language

### After Week 2:
- Add: Delta Lake, pytest, AI-powered SQL generation
- Remove: Putty, Eclipse, Sqoop, Hortonworks

### After Week 3:
- Add: dbt, RAG pipelines, vector databases
- Fix typo: "Clod formation" → "CloudFormation"

### After Week 4:
- Add: Spark Structured Streaming, Kafka, AI-assisted data quality
- Remove: DOB, gender, marital status, passport number

---

## Weekly Review Template

### Week 1 Review
- **What went well:**
- **What tripped me up:**
- **Interview applications sent:** (target: 25-50)
- **Technical calls received:**
- **Priority for Week 2:**

### Week 2 Review
- **What went well:**
- **What tripped me up:**
- **Interview applications sent:** (cumulative)
- **Technical calls received:**
- **Priority for Week 3:**

### Week 3 Review
- **What went well:**
- **What tripped me up:**
- **Interview applications sent:** (cumulative)
- **Interviews scheduled:**
- **Priority for Week 4:**

### Week 4 Review
- **What went well:**
- **What tripped me up:**
- **Total applications sent:**
- **Interviews completed:**
- **Offers/next rounds:**
- **Next steps:**

---

## Amendment Instructions

This is a living document. You can:
- Add new tasks: copy the `[ ]` checkbox format
- Skip tasks: change `[ ]` to `[~]` with reason
- Reorder within a week
- Adjust time allocations based on what's working

Update `CLAUDE.md` "Current Progress" section to point here when you start Phase 0.
