As lead data engineer:
I have created short notes on the basis of my memory and study please review and correct them:
Review and correct where ever required
Add example and details whereever required
Add index which I can use for quick revision
Create the notes in MD format

Data lake issues no atomic read. No ACID, Slow listing, Partition evolution is next to impossible
schema evolution is not easy, no time travel

To solve these issue and et and totally Engine agnostics, Partition evolution support
Iceberg Open table format got create 
Metadata layer

- Metadata file: Table schema partition etc snapshots
- Manifest List: Track list of manifest file for snapshots
- Manifest file: Individual data file stats and partition value

Snapshot: Immutable data file at a point of time is called snapshot in case of update delete or addition new snapshot get created
Hidden partition: Iceberg hide the partition write and pruning which help later in schema evolution Iceberg itself take care of partitioning
Partition evolution: Since partitions are controlled by Iceberg it gives unique feature of partition evolution where change in partition do not require rewriting the entire data but new data structure chagnes and old data can be fetcched from existing structure only. However in longer run for performance it is suggested to update and rewrite the data.

Partition transform: partition is metadata rule which define how a column is mapped to a physical partition layout
instead of create new or modifi column declaring partition transform at write time organise the file. There are build in partition transform
Temporal transforms(time base)
Bucketing
Truncate
Identity

Schema evolution: Iceberg support full schema evolution add update remove or enhance the column

Snapshot isolation/Time travel: Since iceberg keep track of snapshots and theire changes it allows feature of timetravel where we can go and fetch data in past by timestamp of snapshot version
catalog: Iceberg require exernal catalog Glue catalog or HIve metastore etc.
Compacation: Due to frequent write update iceberg table might accumulate multiple small files combining them is compaction hich boost performance
Snapshot exiration removing old unused data snapshot removal for claing storage and performance
Optimisation suggetion:
Use bucketing
Frequently rewrite data file after multiple update or addition
Frequently rewrite manifest file after multiple update or addition
Use hidden partitions

Frequently asked:

What problem does Iceberg solve that Hive tables don't?
Explain Iceberg's metadata layer structure (metadata file → manifest list → manifest files).
What is hidden partitioning and why does it matter?
What is partition evolution and how is it different from Hive's fixed partitioning?
How does Iceberg achieve time travel and snapshot isolation?
What's the difference between Iceberg and Delta Lake?

Scenario-based:

Your table's monthly partitions have grown too large for efficient queries — how do you fix this without downtime, using Iceberg?
You need Spark, Trino, and Snowflake to all read/write the same table without duplicating data — how would you design this?
A table has accumulated thousands of small files from streaming writes — what commands/procedures would you use to fix it?

Lead Data Engineer design questions:

How would you design a multi-engine Lakehouse platform (Spark, Trino, Flink) using Iceberg, including catalog choice and governance?
Compare Iceberg, Delta Lake, and Hudi — how would you decide which to adopt for a new platform, and what factors matter most?
How would you design a migration path from an existing Hive-based data lake to Iceberg with minimal downtime and no data loss?
How do you design snapshot expiration and compaction schedules to balance cost, compliance/audit requirements, and query performance?

Common follow-ups:

What catalog would you choose in an AWS-native environment vs a multi-cloud environment, and why?
How does Iceberg handle concurrent writes from two different engines (e.g., Spark and Flink) at the same time?
What happens to query performance if you never run expire_snapshots or rewrite_manifests?