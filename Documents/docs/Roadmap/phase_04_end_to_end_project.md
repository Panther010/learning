# Phase 4: End-to-End Project (Ecommerce Pipeline)

**Target**: Weeks 19-24 | ~36 hours total | 5-7 hrs/week

<!--
AMENDABLE: Add, remove, or reorder tasks freely.
This phase builds a production-like data pipeline from scratch: Docker, Kafka, Spark, medallion architecture.
-->

## Goals
- Build a real-world streaming + batch pipeline
- Medallion architecture: bronze → silver → gold
- Docker Compose for local development
- Kafka integration for streaming
- Data quality checks between layers
- Complete documentation and testing

## Tasks

### 4.1 Design the pipeline architecture
- [ ] **Status: Not Started**
- **What to do**: Design a 3-layer medallion architecture for an ecommerce dataset (users, products, orders, events). Document the architecture with a diagram.
- **What to learn**: Medallion architecture pattern (bronze = raw, silver = cleaned, gold = aggregated). Why layering matters. Data lineage.
- **Research**: Medallion architecture articles. Delta Lake best practices.
- **Deliverable**: `projects/ecommerce_pipeline/docs/architecture.md` with Mermaid diagram
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 4.2 Create synthetic data generator
- [ ] **Status: Not Started**
- **What to do**: Write a Python script that generates realistic ecommerce data (users, products, orders, clickstream events). Make it configurable for volume.
- **What to learn**: Synthetic data generation patterns. Faker library or manual generation. Referential integrity (orders reference users and products).
- **Deliverable**: `projects/ecommerce_pipeline/scripts/generate_data.py`
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 4.3 Docker Compose setup
- [ ] **Status: Not Started**
- **What to do**: Create docker-compose.yml with services: Kafka, Zookeeper, Spark, PostgreSQL (for gold layer).
- **What to learn**: Docker Compose multi-service orchestration. Service dependencies. Volume mounts. Network configuration.
- **Research**: Docker Compose documentation. Kafka Docker images. Spark Docker images.
- **Deliverable**: `projects/ecommerce_pipeline/docker-compose.yml` that spins up all services
- **Acceptance criteria**: `docker-compose up -d` starts all services successfully
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 4.4 Bronze layer: ingest raw data
- [ ] **Status: Not Started**
- **What to do**: Write Spark job that reads raw CSV/JSON files and writes to Delta Lake bronze tables with minimal transformation (schema validation, add ingestion timestamp).
- **What to learn**: Bronze layer patterns. Schema enforcement. Idempotent ingestion. Handling bad records.
- **Deliverable**: `projects/ecommerce_pipeline/src/bronze/ingest_*.py` for each entity
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 4.5 Silver layer: cleanse and conform
- [ ] **Status: Not Started**
- **What to do**: Write Spark jobs that read from bronze, apply data quality rules (dedup, null handling, type casting), and write to silver Delta tables.
- **What to learn**: Silver layer patterns. Data quality enforcement. SCD Type 1 vs Type 2. Slowly changing dimensions.
- **Deliverable**: `projects/ecommerce_pipeline/src/silver/process_*.py` for each entity
- **Estimated time**: 4 hours
- **Come back for review**: Yes

### 4.6 Gold layer: business aggregations
- [ ] **Status: Not Started**
- **What to do**: Write Spark jobs that create business-level aggregations: revenue by product, conversion funnel, customer lifetime value, top products by region.
- **What to learn**: Gold layer patterns. Dimensional modeling. Star schema. Pre-aggregation for BI tools.
- **Deliverable**: `projects/ecommerce_pipeline/src/gold/aggregate_*.py`
- **Estimated time**: 4 hours
- **Come back for review**: Yes

### 4.7 Kafka producer for clickstream events
- [ ] **Status: Not Started**
- **What to do**: Write a Kafka producer that simulates real-time user clickstream events (page views, add-to-cart, checkout).
- **What to learn**: Kafka producer API. Message serialization (JSON or Avro). Partitioning strategy.
- **Research**: kafka-python library. Producer configuration.
- **Deliverable**: `projects/ecommerce_pipeline/scripts/clickstream_producer.py`
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 4.8 Streaming job: process clickstream
- [ ] **Status: Not Started**
- **What to do**: Write Structured Streaming job that reads from Kafka, processes events (windowed aggregations), writes to Delta tables.
- **What to learn**: Kafka source for Structured Streaming. Windowing in streaming. Handling late data. Checkpointing.
- **Deliverable**: `projects/ecommerce_pipeline/src/streaming/process_clickstream.py`
- **Estimated time**: 4 hours
- **Come back for review**: Yes

### 4.9 Data quality framework
- [ ] **Status: Not Started**
- **What to do**: Create a simple data quality framework that validates data between layers (null checks, range checks, referential integrity, uniqueness).
- **What to learn**: Data quality patterns. When to fail vs warn. Quality metrics collection.
- **Deliverable**: `projects/ecommerce_pipeline/src/quality/` with reusable quality check functions
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 4.10 End-to-end orchestration script
- [ ] **Status: Not Started**
- **What to do**: Create a script that runs the full pipeline: start Docker services, generate data, run bronze→silver→gold jobs, run streaming job, verify outputs.
- **What to learn**: Pipeline orchestration without Airflow. Dependency management. Error handling and retries.
- **Deliverable**: `projects/ecommerce_pipeline/scripts/run_pipeline.py`
- **Acceptance criteria**: Script runs full pipeline end-to-end without errors
- **Estimated time**: 2.5 hours
- **Come back for review**: Yes

### 4.11 Comprehensive testing
- [ ] **Status: Not Started**
- **What to do**: Write integration tests for each layer. Test data quality framework. Test streaming job with mock Kafka data.
- **What to learn**: Testing data pipelines. Integration tests vs unit tests. Test data generation.
- **Deliverable**: `projects/ecommerce_pipeline/tests/` with good coverage
- **Estimated time**: 4 hours
- **Come back for review**: Yes

### 4.12 Documentation and README
- [ ] **Status: Not Started**
- **What to do**: Write comprehensive README with architecture diagram, setup instructions, how to run, troubleshooting, design decisions.
- **What to learn**: Project documentation best practices. Making projects accessible to others.
- **Deliverable**: `projects/ecommerce_pipeline/README.md`
- **Estimated time**: 2 hours
- **Come back for review**: Yes

---

## Total Estimated Time: ~37 hours
This is your portfolio centerpiece — a complete, production-like data platform.
