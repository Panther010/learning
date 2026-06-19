# Phase 6: Cloud (AWS)

**Target**: Weeks 31-36 | ~36 hours total | 5-7 hrs/week

<!--
AMENDABLE: Add, remove, or reorder tasks freely.
After completing AWS, add phase_07_azure.md and phase_08_gcp.md.
-->

## Goals
- Infrastructure as Code with Terraform
- S3 as data lake storage
- Glue/EMR for processing
- Athena for querying
- Deploy the ecommerce pipeline (or a subset) to AWS

## Tasks

### 6.1 AWS CLI + Terraform setup
- [ ] **Status: Not Started**
- **What to do**: Configure AWS CLI. Create Terraform project with remote state in S3.
- **What to learn**: Terraform fundamentals (providers, resources, state, plan/apply cycle). AWS CLI configuration. Remote state management. Why IaC matters (reproducibility, version control, peer review).
- **Research**: Terraform docs "Getting Started with AWS". AWS CLI docs.
- **Deliverable**: `infrastructure/terraform/` with `main.tf`, `variables.tf`, `backend.tf`. `terraform init` and `terraform plan` work.
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 6.2 S3 data lake buckets
- [ ] **Status: Not Started**
- **What to do**: Terraform to create S3 buckets for raw, processed, and serving layers.
- **What to learn**: S3 bucket policies. Lifecycle rules (transition to Glacier, expiration). Versioning. Server-side encryption. Bucket naming conventions.
- **Deliverable**: Terraform module creating S3 buckets with appropriate policies.
- **Estimated time**: 1.5 hours
- **Come back for review**: Yes

### 6.3 Upload data to S3
- [ ] **Status: Not Started**
- **What to do**: Script using boto3 to upload raw data files to S3.
- **What to learn**: AWS SDK (boto3). S3 upload patterns. Multipart upload for large files. Error handling for cloud operations.
- **Deliverable**: `scripts/upload_to_s3.py`
- **Estimated time**: 1 hour
- **Come back for review**: No

### 6.4 Glue Catalog and Crawler
- [ ] **Status: Not Started**
- **What to do**: Terraform for Glue database and crawler. Crawl S3 raw data to populate the catalog.
- **What to learn**: Glue Data Catalog (the AWS equivalent of Hive metastore). Crawlers (automatic schema detection). Partition discovery. Why a catalog matters (Athena, EMR, and Redshift all query through it).
- **Deliverable**: Terraform module for Glue resources. Crawler successfully populates catalog.
- **Estimated time**: 2 hours
- **Come back for review**: Yes

### 6.5 Glue ETL job
- [ ] **Status: Not Started**
- **What to do**: Port the flight_analysis pipeline to run as a Glue ETL job.
- **What to learn**: Glue job authoring. GlueContext and DynamicFrame. Bookmarks for incremental processing. Job parameters. How Glue differs from plain PySpark.
- **Deliverable**: Glue job script + Terraform to deploy it.
- **Estimated time**: 3 hours
- **Come back for review**: Yes

### 6.6 Athena queries
- [ ] **Status: Not Started**
- **What to do**: Write Athena queries against the Glue catalog tables. Create saved/named queries.
- **What to learn**: Athena (serverless Presto/Trino). Query optimization (partitioning, columnar format benefits). Result caching. Cost model (pay per TB scanned).
- **Deliverable**: SQL files in `infrastructure/athena/` for key analytical queries.
- **Estimated time**: 1.5 hours
- **Come back for review**: No

### 6.7 IAM roles and security
- [ ] **Status: Not Started**
- **What to do**: Proper IAM roles for Glue jobs with least privilege.
- **What to learn**: IAM policies (JSON structure). Roles vs users. Trust policies. Least privilege principle. Why overly broad permissions are a security risk.
- **Deliverable**: Terraform IAM module with properly scoped roles.
- **Estimated time**: 1.5 hours
- **Come back for review**: Yes

### 6.8 Cost monitoring and teardown
- [ ] **Status: Not Started**
- **What to do**: Set up AWS Budgets alert. Document complete teardown process. Create a teardown script.
- **What to learn**: AWS cost management. Tagging strategy. Budget alerts. `terraform destroy`. Why this task exists first (so you don't get a surprise bill).
- **Deliverable**: Terraform budget resource. Teardown script. Documentation.
- **Estimated time**: 1 hour
- **Come back for review**: No

### 6.9 Cloud architecture documentation
- [ ] **Status: Not Started**
- **What to do**: Document the full cloud architecture with diagram. Write an ADR for cloud decisions.
- **What to learn**: Cloud architecture documentation. Mermaid diagrams. Architecture Decision Records.
- **Deliverable**: `infrastructure/README.md` with architecture diagram. `docs/adr/003_aws_architecture.md`.
- **Estimated time**: 1 hour
- **Come back for review**: Yes

### 6.10 EMR cluster (optional, alternative to Glue)
- [ ] **Status: Not Started**
- **What to do**: Terraform for an EMR cluster. Submit the ecommerce Spark jobs to it.
- **What to learn**: EMR architecture (master/core/task nodes). Bootstrap actions. Step submission. Spot instances for cost savings. EMR vs Glue trade-offs.
- **Deliverable**: Terraform EMR module + submit script.
- **Estimated time**: 3 hours
- **Come back for review**: Yes

---

## Total Estimated Time: ~17.5 hours
Cloud + IaC is essential for modern data engineering. After AWS, expand to Azure and GCP.
