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
