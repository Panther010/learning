# Phase 3: Spark Deep Dive

**Target**: Weeks 13-18 | ~36 hours total | 5-7 hrs/week

<!--
AMENDABLE: Add, remove, or reorder tasks freely.
This phase goes deep on PySpark: Delta Lake, optimization, streaming, internals.
-->

## Goals
- Delta Lake for ACID transactions and time travel
- Spark performance optimization techniques
- Structured Streaming fundamentals
- Understanding Spark execution plans
- Production-ready Spark patterns

## Tasks

### 3.1 Delta Lake basics
- [ ] **Status: Not Started**
- **What to do**: Refactor one existing project to use Delta Lake instead of Parquet. Implement basic operations: create, update, delete, upsert.
- **What to learn**: Delta Lake architecture (transaction log, versioning). ACID guarantees on data lakes. Delta vs Parquet tradeoffs. Delta table properties.
- **Research**: Delta Lake documentation. Delta Lake quickstart guide.
- **Deliverable**: One project using Delta Lake with all CRUD operations demonstrated
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 3.2 Delta Lake time travel and versioning
- [ ] **Status: Not Started**
- **What to do**: Implement time travel queries, version history inspection, and rollback in your Delta Lake project.
- **What to learn**: Time travel syntax. Version retention. How Delta stores history. When to use time travel (debugging, auditing, reproducing results).
- **Deliverable**: Examples of reading historical versions, restoring to previous state
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 3.3 Partitioning deep dive
- [ ] **Status: Not Started**
- **What to do**: Create exercises comparing different partitioning strategies. Benchmark query performance with different partition schemes.
- **What to learn**: When to partition. Optimal partition size (128MB-1GB). Over-partitioning vs under-partitioning. Partition pruning. Dynamic partition overwrite.
- **Research**: Spark partitioning best practices. Delta Lake partitioning.
- **Deliverable**: `fundamentals/spark/optimization/partitioning_experiments.py` with benchmarks and findings documented
- **Estimated time**: 3.5 hours
- **Come back for review**: Yes

### 3.4 Broadcast joins and skew handling
- [ ] **Status: Not Started**
- **What to do**: Create examples of broadcast joins and salted joins for handling data skew. Benchmark performance.
- **What to learn**: Broadcast join threshold. When to broadcast manually. Identifying data skew. Salted join pattern. AQE (Adaptive Query Execution).
- **Research**: Spark join strategies. Data skew mitigation techniques.
- **Deliverable**: `fundamentals/spark/optimization/join_strategies.py` with examples
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 3.5 Caching and persistence strategies
- [ ] **Status: Not Started**
- **What to do**: Create examples showing different persistence levels (MEMORY_ONLY, MEMORY_AND_DISK, etc.). Benchmark when caching helps vs hurts.
- **What to learn**: Caching vs checkpointing. Storage levels. When caching is beneficial (reused DataFrames, iterative algorithms). Cache eviction.
- **Deliverable**: `fundamentals/spark/optimization/caching_examples.py` with benchmarks
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 3.6 Explain plans and query optimization
- [ ] **Status: Not Started**
- **What to do**: Practice reading explain plans. Create a guide documenting common patterns and anti-patterns.
- **What to learn**: Physical vs logical plans. Catalyst optimizer. Whole-stage code generation. How to identify bottlenecks from explain plans.
- **Research**: Spark SQL internals. Databricks performance tuning guides.
- **Deliverable**: `docs/notes/spark_explain_plans.md` with annotated examples
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 3.7 Structured Streaming basics
- [ ] **Status: Not Started**
- **What to do**: Refactor the existing batch_word_count to use Structured Streaming with a file source.
- **What to learn**: Streaming vs batch concepts. Structured Streaming model (unbounded tables). Triggers (ProcessingTime, Once, Continuous). Output modes (Append, Complete, Update).
- **Research**: Structured Streaming programming guide.
- **Deliverable**: `fundamentals/spark/streaming/file_streaming_word_count.py`
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 3.8 Windowing and watermarks
- [ ] **Status: Not Started**
- **What to do**: Create a streaming application that does windowed aggregations (tumbling and sliding windows) with watermarks for late data.
- **What to learn**: Event time vs processing time. Watermarks for handling late data. Window functions in streaming. State management.
- **Deliverable**: `fundamentals/spark/streaming/windowed_aggregations.py`
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 3.9 Stateful streaming operations
- [ ] **Status: Not Started**
- **What to do**: Implement a stateful streaming operation using mapGroupsWithState or flatMapGroupsWithState.
- **What to learn**: Stateful processing model. State timeout. State store internals. Use cases (sessionization, deduplication).
- **Research**: Arbitrary stateful processing in Structured Streaming.
- **Deliverable**: `fundamentals/spark/streaming/stateful_processing.py` (e.g., user session tracking)
- **Estimated time**: 4 hours
- **Come back for review**: Yes

### 3.10 SQL in Spark patterns
- [ ] **Status: Not Started**
- **What to do**: Create examples showing when to use SQL vs DataFrame API. Implement the same logic both ways.
- **What to learn**: createOrReplaceTempView. Spark SQL syntax. When SQL is cleaner than DataFrame API. Mixing SQL and DataFrame operations.
- **Deliverable**: `fundamentals/spark/sql_in_spark/` with comparison examples
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 3.11 UDFs and performance implications
- [ ] **Status: Not Started**
- **What to do**: Create examples comparing UDFs vs built-in functions. Show when Pandas UDFs (vectorized) help.
- **What to learn**: UDF serialization overhead. Why built-ins are faster. Pandas UDFs (Arrow-based). When UDFs are necessary vs avoidable.
- **Deliverable**: `fundamentals/spark/optimization/udf_performance.py` with benchmarks
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 3.12 Refactor all projects to use Delta Lake
- [ ] **Status: Not Started**
- **What to do**: Convert flight_analysis, banking_pipeline, yelp_analysis, world_bank_gdp to use Delta Lake.
- **What to learn**: Applying Delta Lake in real projects. Migration patterns. Delta Lake in production.
- **Deliverable**: All portfolio projects using Delta Lake
- **Estimated time**: 5 hours
- **Come back for review**: Yes (per project)

---

## Total Estimated Time: ~36 hours
After this phase, you'll have deep Spark knowledge comparable to specialists.
