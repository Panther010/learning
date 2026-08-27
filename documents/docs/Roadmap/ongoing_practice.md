# Ongoing Practice (Continuous, alongside all phases)

<!--
AMENDABLE: Add new practice goals anytime.
This file runs in parallel with all phases — do a little bit from here every week.
-->

## Weekly Rhythm (suggested, adjust to your energy)
- **Weekdays (3-4 hrs)**: Work on current phase's main tasks
- **1-2 hrs/week**: SQL problem + DS&A review from this list
- **Weekend (optional)**: Small project or documentation catch-up

---

## SQL Practice
- [ ] Continue adding SQL problems (target: 75 total by end of Phase 3, 100 by end of Phase 6)
- [ ] For each new SQL problem, add an entry to `fundamentals/sql/README.md` index
- [ ] Topics to add: PIVOT/UNPIVOT, GROUPING SETS, ROLLUP/CUBE, LATERAL JOIN, JSON functions
- [ ] Create `docs/notes/sql_patterns.md` — a cheat sheet of SQL patterns for interview prep
- [ ] Practice writing the same query in PostgreSQL, MySQL, and Spark SQL (syntax differences)

## DS&A Maintenance
- [ ] Add graph problems: BFS, DFS, topological sort, shortest path (2-3 problems)
- [ ] Add heap problems: min-heap, max-heap, priority queue (2-3 problems)
- [ ] Add dynamic programming: memoization vs tabulation, knapsack, longest common subsequence
- [ ] Add complexity analysis as comments to ALL existing DS&A files (time + space)
- [ ] All new problems MUST have pytest tests and type hints from day one

## Small Python Projects (one per phase, builds skill variety)
- [ ] **Phase 2**: CLI Data Profiler (task 2.8)
- [ ] **Phase 3**: CSV Schema Validator — validates CSV files against a YAML schema definition
- [ ] **Phase 4**: Log Parser — parses and aggregates Spark application logs, outputs summary report
- [ ] **Phase 5**: Config Diff Tool — compares two YAML configs and shows differences (useful for debugging pipeline config issues)
- [ ] **Phase 6**: S3 File Inventory — lists and summarizes S3 bucket contents using boto3

## Interview Prep Integration
- [ ] Create `docs/notes/interview_topics.md` mapping repo content to common interview topics
- [ ] For each DS&A topic, ensure time/space complexity is documented
- [ ] For each SQL problem, add a "Common Interview Variant" note
- [ ] Practice explaining project architecture decisions verbally — record notes in `docs/notes/`
- [ ] Create a "30-minute interview prep" checklist that references specific files to review

## New Topics to Add When Ready
These are topics to explore after the main 6 phases. Add them as new phase files when you're ready:
- [ ] `phase_07_azure.md` — Azure Data Factory, Synapse, ADLS, Databricks
- [ ] `phase_08_gcp.md` — BigQuery, Dataproc, GCS, Cloud Functions, Dataflow
- [ ] `custom_ml_integration.md` — Feature engineering pipelines, MLflow, model serving
- [ ] `custom_data_mesh.md` — Data contracts, data products, platform engineering
- [ ] `custom_llm_pipelines.md` — RAG pipelines, vector stores, embedding pipelines
- [ ] `custom_system_design.md` — System design interview prep for data engineering

---

## Notes
- Check off items as you complete them
- Add new items whenever you discover gaps or interests
- This is YOUR learning journey — customize freely
