# Capco — Lead/Principal Data Engineer Interview Prep
**Interview:** Wed 5 Aug 2026, 11:00–12:30 (GMT+1) · Video, Teams · Interviewer: Tejaswini Pattanshetty

**Approach:** you already know most of this — the goal is revision and solidification, not new learning. Each topic below is a complete concept checklist you can self-test against, plus a ready-to-paste prompt to generate practice Q&A for that specific area. Graph DB / Scala / ML / BI tooling get one honest framing line each — not study time.

---

## 0. Logistics checklist
- [ ] Reply to Radka confirming receipt + attendance (today)
- [ ] Test Teams link, camera, mic, and a quiet room tonight — not Wednesday morning
- [ ] Have a notepad/whiteboard-style tool ready in case they ask you to sketch a schema or architecture on screen

---

## 1. Two-Day Revision Schedule

Tuesday is a full revision day across your known areas. Wednesday morning is light final review only.

### Monday evening
- Skim this whole document once to load the map, no deep work

### Tuesday
| Time              | Focus                                                                                               |
|-------------------|-----------------------------------------------------------------------------------------------------|
| Morning session 1 | Database & Data Warehousing + ETL — self-test against the checklists below                          |
| Morning session 2 | Big Data (Hadoop/Hive/Spark/file formats) — your strongest area, quick pass                         |
| Midday            | Event Driven Systems (Kafka/Spark Streaming) — ties to what you're already studying this week       |
| Afternoon         | Serverless + Cloud Offerings + Python                                                               |
| Late afternoon    | DevOps/Test Automation + Security + Observability                                                   |
| Evening           | Full self-test: go topic by topic below, answer out loud, flag anything shaky and revisit only that |

### Wednesday morning
- Re-read your own project notes (Quantexa ACIC, Aviation SDLF, TCS/BP/StanChart) so concrete stories are fresh
- Prepare 2–3 questions to ask them
- One quick pass on the 4 framing lines (section 3) — 5 minutes, not study

---

## 2. Revision Checklists — Prompt-Ready

For each area, paste the checklist into an AI with: *"Generate Lead/Principal-level interview questions (and brief model answers) covering all of these concepts, so I can self-test."*

### Database & Data Warehousing
- ACID properties, transaction isolation levels
- Normalization/denormalization (1NF–3NF), when to denormalize deliberately
- Indexing strategies: B-tree vs hash, when an index hurts write performance
- OLTP vs OLAP
- Dimensional modelling: star vs snowflake, fact vs dimension tables, grain, conformed dimensions
- SCD Types 1/2/3 (surrogate keys, effective dating)
- SQL vs NoSQL: CAP theorem, document/key-value/wide-column categories, when each wins
- Data lake vs warehouse vs lakehouse, medallion architecture, schema-on-read vs schema-on-write
- Data quality dimensions: completeness, accuracy, consistency, timeliness, uniqueness — and how you'd automate checks for each

### ETL
- Basic transformations: cleansing, dedup, type casting, join/aggregation at scale
- Self-managed (Airflow/NiFi/custom Spark) vs SaaS (Fivetran/Stitch/Talend) — control/cost/maintenance trade-offs
- ETL vs ELT: why cloud warehouses shifted the industry to ELT, when ETL still wins (PII scrubbing pre-landing, compliance)

### Big Data
- HDFS architecture: NameNode/DataNode, replication, why it mattered pre-cloud-object-storage
- MapReduce: map/shuffle/reduce phases, why Spark superseded it
- Hive: metastore, HiveQL, partitioning vs bucketing, its role as a metadata layer today
- Spark: shuffle, partitioning strategy, Catalyst optimizer, broadcast joins, data skew handling, lazy evaluation, DAG execution
- File formats: Parquet vs Avro vs JSON vs ORC — columnar vs row-based, schema evolution support, compression trade-offs, splittability

### Event Driven Systems
- Kafka: topics, partitions, producers/consumers, consumer groups, offset management
- Delivery semantics: at-least-once, at-most-once, exactly-once — how each is actually achieved
- Spark Structured Streaming: micro-batch model, watermarking, checkpointing, output modes (append/update/complete)

### Serverless Functions
- Design considerations: cold starts, statelessness, execution time limits, cost model (invocation-based vs uptime-based)
- When NOT to use serverless: long-running or stateful workloads
- AWS Lambda + Step Functions for orchestration — your SDLF/serverless project experience is your strongest evidence here

### Cloud Offerings
- Ingestion: Kinesis, Glue
- Storage: S3, storage classes
- Processing: EMR, Glue, Dataproc (conceptual GCP awareness)
- Warehousing: Redshift, BigQuery, Snowflake — trade-offs
- Orchestration: Step Functions, Airflow, Cloud Composer

### Python
- Pandas: DataFrame ops, vectorization vs loops, memory limits at scale
- NumPy: arrays vs lists, broadcasting
- Matplotlib: basic plotting — light-weight, unlikely to go deep

### Test Automation and DevOps
- CI pipeline stages: build → test → deploy, applied to data pipelines specifically
- Data-pipeline-specific testing: schema validation, data contract tests, not just unit tests — your pytest/Delta Lake project is direct evidence here

### Security
- Encryption: at-rest vs in-transit, symmetric vs asymmetric
- TLS: what it protects, where it sits in a pipeline (API calls, JDBC)
- Secrets management: Secrets Manager/Vault vs hardcoding
- GDPR/PII: data minimization, right to erasure, pseudonymization/anonymization — your entity-resolution background is strong, relevant evidence here

### Observability
- SLAs/SLOs for freshness and completeness
- Alerting on schema drift, volume anomalies
- Lineage tracking
- Ties directly to your DQ tooling experience — good place to reach for a real example

---

## 3. The 4 gap areas — one honest framing line each, not study material

Say these plainly if asked; don't try to fake depth.

- **Graph Databases:** *"I haven't built production graph DB systems, but I understand the modelling paradigm — relationships as first-class citizens rather than foreign keys — and where it wins, like entity resolution work such as my Quantexa ACIC project, where relationship traversal at scale is exactly the graph use case."*
- **Scala:** *"My hands-on depth is in PySpark, but I know Spark itself is written in Scala and native Scala jobs avoid the JVM-Python serialization overhead PySpark carries — that's a trade-off I'd weigh on a performance-critical pipeline."*
- **Machine Learning:** *"My role has been building and validating the pipelines that feed models — feature data quality, freshness, lineage — rather than building models myself. I understand the supervised/unsupervised/reinforcement distinction at a conceptual level."*
- **BI Tooling:** *"I haven't built dashboards directly in PowerBI or Looker, but I've built the warehouse layer that feeds BI tools — grain, conformed dimensions, distribution/sort keys in Redshift — which is what actually makes a warehouse BI-ready."*


𝗣𝘆𝘁𝗵𝗼𝗻

1. List vs Tuple vs Set vs Dictionary
2. Deep Copy vs Shallow Copy
3. *args and **kwargs usage
4. Lambda, Map, Filter, Reduce
5. Generators vs Iterators
6. Decorators in Python
7. Multithreading vs Multiprocessing
8. Exception Handling Best Practices
9. Memory Management and Garbage Collection

𝗦𝗤𝗟

10. ROW_NUMBER vs RANK vs DENSE_RANK
11. CTE vs Subquery
12. DELETE vs TRUNCATE vs DROP
13. INNER vs LEFT vs FULL JOIN
14. Clustered vs Non-Clustered Index
15. WHERE vs HAVING
16. Window Functions in SQL
17. Query Performance Optimization
18. Primary Key vs Unique Key

𝗣𝘆𝗦𝗽𝗮𝗿𝗸

19. Repartition vs Coalesce
20. groupByKey vs reduceByKey
21. Narrow vs Wide Transformations
22. Cache vs Persist
23. Broadcast Join in PySpark
24. DataFrame vs RDD
25. Handling Data Skew in Spark
26. Delta Lake MERGE Operations




1. Data Engineering fundamentals — Days 1–15
ETL vs ELT — when to use each
OLTP vs OLAP --> Done
Data Warehouse vs Data Lake
Data Lake vs Data Lakehouse
Structured vs Semi-structured vs Unstructured data
Batch vs Streaming processing
Full Load vs Incremental Load
CDC — Change Data Capture
Slowly Changing Dimensions — Type 1 vs Type 2
Fact vs Dimension tables
Star Schema vs Snowflake Schema
Normalization vs Denormalization
Surrogate Key vs Natural Key
Idempotency in data pipelines
What makes a data pipeline production-ready?
2. SQL — Days 16–25
WHERE vs HAVING
INNER vs LEFT vs RIGHT vs FULL JOIN
UNION vs UNION ALL
Window Functions — ROW_NUMBER, RANK, DENSE_RANK
LEAD and LAG — real-world use cases
CTE vs Subquery
EXISTS vs IN
Correlated Subqueries
SQL Query Execution Order
SQL Query Optimization — practical checklist
3. Data modelling & warehousing — Days 26–35
How to design a dimensional model
Grain of a fact table — why it matters
Degenerate Dimensions
Role-playing Dimensions
Conformed Dimensions
Bridge Tables
Factless Fact Tables
Snapshot vs Transaction Fact Tables
Late-arriving dimensions
Handling schema changes in data warehouses
4. Spark / PySpark — Days 36–50

This is where you can really demonstrate your existing expertise.

Spark architecture — Driver, Executors, Cluster Manager
Transformation vs Action
Narrow vs Wide Transformations
What causes a Spark Shuffle?
Spark Partitioning explained
Repartition vs Coalesce
Broadcast Join — when and why
Sort-Merge Join
Data Skew — the silent Spark performance killer
Salting to solve data skew
Spark Cache vs Persist
Catalyst Optimizer
Adaptive Query Execution — AQE
Spark file formats — Parquet vs ORC
How I would troubleshoot a slow Spark job

Your Spark posts should go beyond definitions.

For example, instead of:

"What is repartition?"

Do:

Repartition vs Coalesce: a decision that can save your Spark job from unnecessary shuffle

Then show a small example and explain the trade-off.

5. AWS / Cloud Data Engineering — Days 51–60
S3 as a Data Lake
S3 partitioning strategy
AWS Glue vs EMR
Athena — how it works
Redshift vs Athena
Glue Data Catalog
AWS Lambda in data pipelines
Step Functions vs Airflow
EventBridge for event-driven data pipelines
Designing a serverless AWS data pipeline
6. Modern Data Stack — Days 61–70
dbt — what problem does it solve?
dbt vs traditional ETL
dbt Models, Tests and Sources
Data lineage
Data quality vs data validation
Data observability
Data contracts
Schema evolution
Medallion Architecture — Bronze/Silver/Gold
Lakehouse Architecture
7. Streaming & real-time data — Days 71–82

These topics are particularly useful if you want to move toward Staff/Principal-level roles.

Kafka architecture
Kafka Topic vs Partition
Kafka Consumer Groups
Kafka Offset management
At-most-once vs At-least-once vs Exactly-once
Event-driven architecture
Event time vs Processing time
Watermarks in streaming
Windowing in streaming
Apache Flink vs Spark Structured Streaming
Batch vs Micro-batch vs True Streaming
Designing a real-time data pipeline
8. Data Engineering system design — Days 83–92

This is the category I'd particularly recommend for you as a Lead Data Engineer.

How to design a scalable data platform
Designing a 1 TB/day pipeline
Designing a 10 TB/day pipeline
Designing an incremental ingestion framework
Designing a CDC pipeline
Designing a real-time analytics platform
Designing a metadata-driven pipeline
Designing a fault-tolerant data pipeline
Designing an idempotent pipeline
Designing a multi-tenant data platform
9. AI + Data Engineering — Days 93–100

Since you're learning AI, connect it to your existing strength rather than trying to become a generic AI influencer.

What is an embedding?
Vector databases explained
RAG — Retrieval Augmented Generation
RAG pipeline architecture
Data Engineering challenges in RAG
Chunking strategies for RAG
Batch vs real-time feature pipelines for AI
How Data Engineers fit into the AI/LLM ecosystem


Hook → Concept → Real-world example → Trade-off → Takeaway


For example:

Why does Spark become slow even when your code looks perfectly fine?

One common reason: data skew.

Imagine joining 500M transactions with customer data.

If one customer represents 30% of all transactions, Spark may send a huge amount of data to a single partition.

Most executors finish quickly.

One executor keeps running.

Your entire job waits for it.

This is the classic straggler problem caused by skew.

Possible approaches:

Broadcast join where appropriate
Salting
Better partitioning
AQE skew join handling

Key lesson:
Distributed processing doesn't automatically mean evenly distributed processing.

The real skill is understanding how data moves across the cluster.

That kind of post demonstrates considerably more expertise than:

"Data skew is when data is unevenly distributed."