# Bakul Seth — Job Transition Study Plan

**Created:** 4 June 2026
**Updated:** 7 June 2026
**Goal:** Interview-ready in 4 weeks, Python + PySpark + SQL + AWS + AI
**Status:** In Progress

**📁 Detailed Roadmap:** `/Users/bakulseth/PycharmProjects/learning/docs/roadmap/phase_00_interview_prep.md`
**📁 Learning Repo:** `/Users/bakulseth/PycharmProjects/learning/`

> All your study work gets committed to the learning repo, building your portfolio as you prep.

---

## Daily Routine (7-8 hours)

### Morning — Interview Prep (3 hours)

| Hour | Focus | Details |
|------|-------|---------|
| 1 | SQL | 2 hard LeetCode/HackerRank problems. Window functions, CTEs, self-joins, explain plans. |
| 2 | PySpark | Write transformations from scratch. groupBy, window, join, UDF, broadcast, repartition, caching. |
| 3 | Python DSA + Core | 1 medium LeetCode. Rotate: decorators/generators, collections/itertools, OOP, exception handling, multithreading. |

### Afternoon — Concepts & Design (2.5 hours)

| Hour | Focus |
|------|-------|
| 4 | AWS deep revision (Week 1-2) / System design practice (Week 3-4) |
| 5 | Concept of the day (rotate list below) |
| 5.5 | AI theory (30 min — see AI section) |

**Concept rotation:** Partitioning strategies, Delta Lake vs Parquet, Spark internals (catalyst/tungsten/shuffle), Data modelling (star/snowflake), SCDs, Exactly-once semantics, Backfill strategies.

### Evening — Hands-on (2.5 hours)

| Hour | Focus |
|------|-------|
| 6-7 | Weekly gap filling project |
| 7-8 | AI hands-on project |

### Daily Non-Negotiables (30 min)

- [ ] Apply to 5-10 jobs
- [ ] Update 1 thing on LinkedIn or resume

---

## Week 1 Tracker

### Gap Filling: Docker + Airflow
- [ ] Install Docker Desktop
- [ ] Write a Dockerfile for a PySpark job
- [ ] Create docker-compose with Spark + Postgres
- [ ] Install Airflow in Docker (astro CLI or docker-compose)
- [ ] Write first DAG that triggers PySpark job
- [ ] Add retries and alerting to DAG

### AI: Claude API Basics
- [ ] Read Anthropic API docs (docs.anthropic.com)
- [ ] Get API key, install `anthropic` Python SDK
- [ ] Write Python script: send prompt, get response
- [ ] Add system prompts to control output
- [ ] Implement prompt caching
- [ ] Experiment with structured output (JSON mode)

### AI Theory (30 min/day)
- [ ] Mon: Prompt engineering patterns — few-shot, chain-of-thought, role prompting
- [ ] Tue: RAG overview — vector embeddings, chunking, retrieval
- [ ] Wed: LLM fundamentals — tokens, context windows, temperature, top-p
- [ ] Thu: AI in data engineering — quality checks, schema inference, SQL generation
- [ ] Fri: AI tools landscape — LangChain, LlamaIndex, ChromaDB, Pinecone

### Interview Prep
- [ ] SQL: 10 hard problems done
- [ ] PySpark: 5 transformation exercises done
- [ ] Python: 5 medium LeetCode done
- [ ] AWS: Glue, EMR, Lambda revised
- [ ] AWS: S3, Redshift, Athena revised

---

## Week 2 Tracker

### Gap Filling: Delta Lake + Testing
- [ ] Convert a PySpark exercise to read/write Delta format
- [ ] Practice MERGE, time travel, Z-ordering
- [ ] Install pytest + chispa
- [ ] Write unit tests for 2-3 PySpark transformations
- [ ] Explore Great Expectations or Soda basics

### AI: SQL Generator Tool
- [ ] Design the tool: input = table schema + question, output = SQL
- [ ] Build schema parser (read DDL or describe table)
- [ ] Send schema + question to Claude API with structured prompt
- [ ] Test generated SQL against known answers
- [ ] Add error handling and retry logic
- [ ] Push to learning repo

### AI Theory (30 min/day)
- [ ] Mon: Vector databases — embeddings, cosine similarity, use cases
- [ ] Tue: MCP architecture — servers, tools, resources
- [ ] Wed: AI agents — tool use, multi-step reasoning
- [ ] Thu: Responsible AI — hallucination, grounding, evaluation
- [ ] Fri: Cost & architecture — token pricing, caching, model selection

### Interview Prep
- [ ] SQL: 10 more hard problems (20 total)
- [ ] PySpark: 5 more exercises (10 total)
- [ ] Python: 5 more LeetCode (10 total)
- [ ] AWS: Step Functions, EventBridge, IAM revised
- [ ] System design: Design a data lake (paper)

---

## Week 3 Tracker

### Gap Filling: dbt Basics
- [ ] Complete dbt fundamentals course (free)
- [ ] Install dbt-core with DuckDB adapter
- [ ] Build a small project: raw → staging → marts
- [ ] Add dbt tests (unique, not_null, relationships)
- [ ] Write a custom dbt test

### AI: Simple RAG Pipeline
- [ ] Install ChromaDB
- [ ] Chunk your DQ/DG documentation into sections
- [ ] Generate embeddings and store in ChromaDB
- [ ] Build retrieval: question → top-k chunks
- [ ] Send chunks + question to Claude API for answer
- [ ] Test with 10 questions about DQ/DG tools

### Interview Prep
- [ ] SQL: 10 more (30 total)
- [ ] PySpark: 5 more (15 total)
- [ ] Python: 5 more (15 total)
- [ ] System design: Design a real-time fraud pipeline
- [ ] System design: Design a CDC system

---

## Week 4 Tracker

### Gap Filling: Streaming
- [ ] Set up Kafka locally (Docker)
- [ ] Produce messages to a topic (Python producer)
- [ ] Spark Structured Streaming: read from Kafka topic
- [ ] Transform stream data
- [ ] Write to Delta Lake sink
- [ ] Understand watermarks and checkpointing

### AI: Data Quality Assistant
- [ ] Build CSV/Parquet profiler (basic stats in Python)
- [ ] Send profile to Claude API for quality assessment
- [ ] Parse Claude's response into structured recommendations
- [ ] Combine with your DQ tool knowledge
- [ ] Add CLI interface
- [ ] Push to learning repo as portfolio project

### Interview Prep
- [ ] SQL: 10 more (40 total)
- [ ] PySpark: 5 more (20 total)
- [ ] Python: 5 more (20 total)
- [ ] System design: Design a data warehouse migration
- [ ] Mock interview practice: STAR format for key stories

---

## Interview Stories to Practice

- [ ] **DQ/DG product ownership** — "I owned two product tools end-to-end, from design to user demos, processing 100M+ rows"
- [ ] **Solo resilience** — "My entire team was offboarded and I kept the product alive solo for 4 weeks, resolving all half-done tickets"
- [ ] **Cross-domain delivery** — "I've delivered across aviation (BP), banking (Standard Chartered), and law enforcement (ASICS)"
- [ ] **AI-assisted development** — "I use AI agents with structured project context (CLAUDE.md), MCP integrations, and prompt engineering daily"
- [ ] **4 AWS certifications** — Proves self-driven learning ability

---

## Resume To-Do

- [ ] Add AI/LLM skills: Claude API, prompt engineering, RAG, MCP
- [ ] Remove dated tools: Putty, Eclipse, Sqoop, Hortonworks, Control-M
- [ ] Fix typo: "Clod formation" → "CloudFormation"
- [ ] Remove personal info: DOB, gender, marital status, passport number
- [ ] Rewrite summary: remove "aspiring to take on senior roles" — you ARE senior
- [ ] Add Docker, Airflow, Delta Lake, dbt as you learn them

---

## Resources

| Resource | Link |
|----------|------|
| Anthropic API Docs | docs.anthropic.com/en/docs/build-with-claude |
| Anthropic Prompt Guide | docs.anthropic.com/en/docs/build-with-claude/prompt-engineering |
| dbt Fundamentals | courses.getdbt.com |
| ChromaDB Docs | docs.trychroma.com |
| DeepLearning.AI Courses | deeplearning.ai/short-courses (free) |
| LeetCode SQL | leetcode.com/problemset/database |
| Delta Lake Docs | docs.delta.io |
| Airflow in Docker | airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose |

---

## Weekly Review

### Week 1 Review
- What went well:
- What tripped me up:
- Priority for next week:

### Week 2 Review
- What went well:
- What tripped me up:
- Priority for next week:

### Week 3 Review
- What went well:
- What tripped me up:
- Priority for next week:

### Week 4 Review
- What went well:
- What tripped me up:
- What to keep deepening:
