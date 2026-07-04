## AWS S3

S3 is not file system but object store where everything is key value pair '/' are naming convetion which give illution of directory structure
Storage clease:
- S3 standara
- S3 Standard -IA
- S3 Intelligent-Tiering
- S3 Glacier
- S3 Glacier Flexible
- Glacer Deep archive

Using life cycle can save cost increase efficiency. Version help keeping old version. Version files dont gete delete only marker get addaed

Encryption SSE-S£, SSE-KMS, SSE-C, Client-Side

Bucket policies — resource-based, attached to the bucket, controls who can access from outside the account
IAM Policies - attached to users/roles, controls what that identity can do:
Pre-signed URL temp access
Multiplar upload increase upload steep mendatory data greater than 5GB
S3 transfer accelarator
Byte fetch S3 select


## AWS Glue
AWS glue is combination of Glue catalog -> Mete adta, Glue crawler schema discovery, Glue ETL jobs servereless spark (Python pyspark spark JOB)

Catalog-> Database table location columnsfile details and partitions
Crawler: Connects to a data source (S3, RDS, JDBC)
Samples the data
Infers the schema
Creates or updates tables in the Glue Catalog
Detects new partitions on subsequent runs
amicFrame vs DataFrame:
python# Glue DynamicFrame — Glue's own abstraction
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database="flights_db", table_name="raw_flights"
)

# Convert to standard PySpark DataFrame for transformations
df = dynamic_frame.toDF()

# Do your PySpark transformations
df_clean = df.filter(col("delay") > 0)

# Convert back to write via Glue
output = DynamicFrame.fromDF(df_clean, glueContext, "output")
Why DynamicFrame exists: It handles schema inconsistencies — missing fields, mixed types — without failing. It uses choice types for ambiguous columns. In practice most engineers convert to DataFrame immediately because standard PySpark is more powerful and familiar.
Glue job types:
TypeUse caseSparkLarge-scale batch transformationsSpark StreamingNear-real-time processingPython ShellLightweight scripts, no Spark neededRayML workloads

Glue book mark: Help to track which data is already processed help in partition  prooning
worker type g1.x(4,16), g2.x(8, 32), g4.x(16, 64)

Glue triggers and orchestration
Data quality
Glue Studio
Connection

## AMAZON EMR:
Elstic mapreduce manager SPARK haddop cluster. EC2, EKS or serverless
Before EMR, running Hadoop/Spark on AWS meant manually provisioning EC2 instances,
Master NOde -> Driver
Core Nodes (HDFS + Compute worker)
Task NOde (Compute only spot instances)

Transient vs Long-running clusters — major interview topic:
Managed Scaling (modern, recommended) 
Auto Scaling (legacy) 
Performance considerations
Cost optimization


## Amazon Redshift
Redshift is AWS's managed MPP (Massively Parallel Processing) data warehouse  OLAP
Leader node
Compute node
Slices

Column-store storage
Distribution keys
Zone map
Distribution style
Zone maps
Workload management: query queue management, prioritization
Redshift spectrum: query data directly in S3 without loading into Redshift
1. Leader node receives query, parses, optimizes
2. Query compiled into compiled C++ code per node (yes — Redshift compiles queries)
3. Compiled code distributed to compute nodes
4. Each node executes against its local slices in parallel
5. Intermediate results from each node sent back to leader
6. Leader performs final aggregation/merge, returns to client

Distribution stype
even, key and all

sort Keys
Scaling performance