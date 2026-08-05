# Apache Hive — Complete Revision Notes
*(Organized basic → advanced: what Hive is → architecture → working with tables → data organization → querying → performance → troubleshooting)*

---

# PART 1 — Hive Fundamentals

## 1. What Is Apache Hive?

**Apache Hive** is an **open-source data warehouse system built on top of Hadoop HDFS**. It was originally created at **Facebook** to let people query huge datasets stored in Hadoop using a **SQL-like language**, instead of writing raw MapReduce code by hand.

- Used for **querying and analyzing large datasets** stored in Hadoop.
- Can process both **structured and semi-structured** data.
- Provides **HiveQL (HQL)** — a SQL-like query language, so people who already know SQL can work with "Big Data" without learning MapReduce.
- Runs on top of **HDFS** (storage) and (historically) **MapReduce** (processing engine) — though newer setups often use **Tez** or **Spark** as the execution engine instead (see §12).

> Think of Hive as a **translator**: you write familiar-looking SQL, and Hive converts it behind the scenes into distributed jobs (MapReduce/Tez/Spark) that run across a Hadoop cluster.

**Schema-on-Read**
This is a core Hive concept, worth understanding well:
- Data is simply stored in HDFS as-is (e.g., a CSV file) — **no schema is enforced when the data is written**.
- The **schema (table structure) is only applied when you read/query the data** — Hive interprets the raw files according to the schema definition you've given it in the Metastore.
- This is the opposite of traditional databases, which use **schema-on-write** (data must match the schema *before* it's even inserted).
- **Trade-off:** schema-on-read is flexible and fast to load data (just drop files in HDFS), but a badly-formatted row won't fail until you actually query it — errors surface later, not at load time.
- The **schema itself is stored in the Metastore** (see below), not in the data files themselves (except for self-describing formats like Parquet/Avro/ORC).

---

## 2. Hive Architecture

| Component | Role |
|---|---|
| **UI (User Interface)** | What the user interacts with to write and submit HiveQL queries (CLI, Beeline, Hue, etc.). |
| **Driver** | Receives the query from the UI and manages its entire lifecycle (session handles, compiles, executes). |
| **Compiler (HQL Processing Engine)** | Parses the query, checks syntax, and builds an execution plan. |
| **Metastore** | Stores **metadata** — database/table definitions, schemas, column types, partition info, and where the actual data lives in HDFS. |
| **Execution Engine** | Converts the compiled query plan into jobs (MapReduce, Tez, or Spark) and executes them against the cluster. |

**Step-by-Step Query Flow**
1. The Hive interface (UI) sends a query to the **Driver**.
2. The Driver uses the **Compiler** to parse the query and check syntax.
3. The Compiler sends a **metadata request** to the **Metastore**.
4. The Metastore returns the relevant metadata (table schema, partitions, location, etc.).
5. The Compiler builds an execution **plan** and sends it back to the Driver.
6. The Driver sends the plan to the **Execution Engine**.
7. The Execution Engine submits the job (e.g., to the Hadoop **JobTracker**/YARN) and performs any needed metadata operations at the Metastore.
8. Once execution finishes, the engine retrieves results from the **DataNodes**.
9. Results are sent back to the Driver, which forwards them to the UI for the user to see.

> Simple mental model: **UI = the "front desk"** taking your request, **Driver = the "project manager"** coordinating everything, **Metastore = the "filing cabinet"** holding table definitions, **Execution Engine = the "workers"** who actually crunch the data on the cluster.

---

## 3. Common Hadoop Filesystem Commands

Since Hive sits on top of HDFS, it's useful to know the basic Hadoop commands for interacting with the filesystem directly:

| Command | What it does |
|---|---|
| `hadoop fs -ls <path>` | List files/directories. |
| `hadoop fs -put <local> <hdfs>` | Upload a file from local disk to HDFS. |
| `hadoop fs -cat <file>` | Print a file's contents. |
| `hadoop fs -tail <file>` | Show the last part of a file (useful for logs). |
| `hadoop fs -mkdir <path>` | Create a directory in HDFS. |
| `hadoop fs -mv <src> <dest>` | Move/rename a file or directory. |
| `hadoop fs -chmod <perm> <path>` | Change file/directory permissions. |
| `hadoop fs -rm -r <path>` | Delete a directory recursively. |

---

# PART 2 — Databases & Tables

## 4. Database Commands

```sql
CREATE DATABASE IF NOT EXISTS <db_name> COMMENT "description";
SHOW DATABASES;
DESCRIBE <db_name>;
DESCRIBE EXTENDED <db_name>;      -- more detail
USE <db_name>;
DROP DATABASE <db_name>;
DROP DATABASE <db_name> CASCADE;  -- also drops all tables inside it
```

---

## 5. Types of Tables in Hive

**1. Managed (Internal) Table** — the default table type.
- Hive manages **both the data and the metadata**.
- Data is stored in Hive's own warehouse directory: `/user/hive/warehouse` (default location).
- **Dropping the table deletes the actual data too**, not just the metadata.
- Use when Hive "owns" the data exclusively.

**2. External Table**
- Only the **metadata** is stored in the Hive warehouse; the **actual data lives elsewhere in HDFS** (a location you specify).
- **Dropping the table only removes the metadata** — the underlying data file is untouched.
- Ideal when the **same data needs to be shared** with other tools/applications (e.g., HBase, Pig) outside of Hive.
```sql
CREATE EXTERNAL TABLE my_table (...)
LOCATION 'hdfs:///some/external/path';
```

**3. Temporary Table**
- Used to hold temporary/scratch data.
- **Automatically deleted at the end of the session.**
- Tagged per-user, so different users can each have their own temp table with the same name without conflicting.
- ⚠️ A temp table can share a name with a permanent table — but while the temp table exists, **the permanent table of the same name becomes inaccessible** for that session.

> Quick comparison: **Managed** = Hive owns everything (data + metadata). **External** = Hive only tracks metadata; data lives independently. **Temporary** = session-scoped scratch table, gone when you disconnect.

---

## 6. Table Creation — Basic Parameters

```sql
CREATE TABLE my_table (
  id INT,
  name STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION '/user/data/my_table';
```
- **`ROW FORMAT DELIMITED`** — tells Hive each line in the source file = one row in the table.
- **`FIELDS TERMINATED BY`** — the column delimiter (default is comma if unspecified).
- **`LOCATION`** — the HDFS directory path where the table's data lives.

**Inspecting a table**
```sql
DESCRIBE <table_name>;              -- basic column info
DESCRIBE FORMATTED <table_name>;    -- full details: type, location, storage format, etc.
SHOW CREATE TABLE <table_name>;     -- regenerates the CREATE statement
```

**Altering a table**
```sql
ALTER TABLE <table> ADD COLUMNS (<col_name> <col_type>);
ALTER TABLE <table> CHANGE COLUMN <old_name> <new_name> <new_type>;
ALTER TABLE <table> RENAME TO <new_table_name>;
ALTER TABLE <table> SET FILEFORMAT avro;
ALTER TABLE <table> SET LOCATION 'hdfs:///new/location';
DROP TABLE <table>;
```

---

## 7. Hive Data Types

**Numeric:** `TINYINT`, `SMALLINT`, `INT`, `BIGINT`, `FLOAT`, `DOUBLE`, `DECIMAL`

**Text:** `CHAR` (fixed length), `VARCHAR` (variable, max length), `STRING` (variable, no max)

**Other primitive types:** `TIMESTAMP` (Unix timestamp), `DATE`, `BINARY`, `BOOLEAN`, `UNIONTYPE`

**Complex Data Types**
| Type | Meaning | Example |
|---|---|---|
| **Array** | Ordered list of values (same type) | `ARRAY<STRING>` → `['apple', 'banana']` |
| **Map** | Key-value pairs | `MAP<STRING, INT>` → `{'age': 30}` |
| **Struct** | A group of named fields, each with its own type (like a mini-record inside a column) | `STRUCT<name:STRING, age:INT>` |

---

# PART 3 — Organizing Data for Performance

## 8. Partitioning

**What is it?**
Partitioning **physically organizes data into separate directories** based on the value of a chosen column. When a query filters (`WHERE`) on that column, Hive only scans the relevant partition(s) instead of the entire table — a big performance win.

**Choosing a partition column**
- Should be a column you **frequently filter or group by** (e.g., `date`, `country`, `region`).
- ❌ Don't partition on a **unique or ever-increasing** column (like an `id`) — that creates too many tiny partitions, which hurts performance instead of helping it.
- Performance improves most when partitions are **roughly equal in size**.

**Static vs. Dynamic Partitioning**
| Type | Behavior |
|---|---|
| **Static** | You explicitly specify the partition value when loading data (you already know it). |
| **Dynamic** | Hive automatically creates partitions **based on the actual column values** in the data being loaded — useful when loading data that spans many partition values at once. |

**Strict vs. Non-strict mode**
- **Strict mode** — every insert must specify **at least one static (non-dynamic) partition** value, as a safety net against accidentally creating a huge number of partitions.
- **Non-strict mode** — allows **all** partition columns to be dynamic.

```sql
-- Loading into a dynamically partitioned table
-- (partition column must be the LAST column, in the correct order)
INSERT INTO TABLE sales PARTITION (country, year)
SELECT amount, product, country, year FROM staging_table;
```

---

## 9. Bucketing

**What is it?**
Bucketing is like a **hash-based index** — it further subdivides data (often within a partition) into a **fixed number of files** based on a hash of a chosen column.

```sql
CREATE TABLE my_table (id INT, name STRING)
CLUSTERED BY (id) INTO 4 BUCKETS;
```
- Hive uses a **hash/modulo** function on the bucketing column to decide which bucket each row goes into.
- All rows with the **same value** in the bucketed column always land in the **same bucket**.
- Best used on a **primary key or unique/high-cardinality column** (unlike partitioning, which avoids unique columns).
- Each bucket = **one physical file** in HDFS.
- The number of reducers used equals the number of buckets.
- ⚠️ Keep the number of buckets reasonable — too many creates excessive small files.

**Advantages of Bucketing**
- **Efficient sampling** of data (see below).
- **Fast, near-random access** to specific data subsets.
- Enables **efficient Map-side joins** (see §13).
- Allows data within each bucket to be **sorted**, enabling efficient **sort-merge joins**.
- Overall, shrinks the amount of data that needs to be scanned/referenced at any given time.

**Data Sampling with Buckets**
```sql
SELECT * FROM table_name TABLESAMPLE (BUCKET 4 OUT OF 4 ON column_name);
-- Fetches only the 4th bucket, assuming the table has 4 buckets total.

SELECT * FROM table_name TABLESAMPLE (BUCKET 1 OUT OF 2 ON column_name);
-- If the table actually has 4 buckets, Hive COMBINES buckets to give you
-- half the data (it can merge or further split buckets as needed).

SELECT * FROM table_name TABLESAMPLE (4 PERCENT);
-- Random % sampling — efficient mainly when the table is NOT bucketed.

SELECT * FROM table_name TABLESAMPLE (2 ROWS);
-- Essentially runs LIMIT under the hood, over the whole table.
```

> Simple way to remember: **Partitioning = separate folders** (coarse-grained, based on a filter-friendly column). **Bucketing = separate files within a table/partition** (fine-grained, hash-based, good for joins/sampling on high-cardinality columns).

---

# PART 4 — Querying Data

## 10. Hive Functions

| Type | Behavior | Examples |
|---|---|---|
| **Standard (Scalar)** | Takes **one row in**, gives **one row out**. | `UPPER()`, `CONCAT()`, date functions |
| **Aggregate** | Takes **many rows in**, gives **one row out** — usually used with `GROUP BY`. | `SUM()`, `COUNT()`, `AVG()` |
| **Table-Generating (UDTF)** | Takes **one row in**, can produce **multiple rows out**. | `EXPLODE()` (commonly used to "unpack" an Array/Map column into multiple rows) |

---

## 11. Hive Joins

| Join Type | Syntax |
|---|---|
| **Inner Join** | `SELECT ... FROM A INNER JOIN B ON A.key = B.key` |
| **Left Join** | `SELECT ... FROM A LEFT JOIN B ON A.key = B.key` |
| **Right Join** | `SELECT ... FROM A RIGHT JOIN B ON A.key = B.key` |
| **Full Outer Join** | `SELECT ... FROM A FULL OUTER JOIN B ON A.key = B.key` |
| **Left Excluding Join** | `... LEFT JOIN B ON A.key=B.key WHERE B.key IS NULL` — rows only in A |
| **Right Excluding Join** | `... RIGHT JOIN B ON A.key=B.key WHERE A.key IS NULL` — rows only in B |
| **Full Excluding Join** | `... FULL OUTER JOIN B ON A.key=B.key WHERE A.key IS NULL OR B.key IS NULL` — rows unique to either side |

**How Hive Actually Executes a Join**
- Hive keeps the **first (left) table in memory** and **streams the second table** for comparison.
- Each join gets converted into a **MapReduce job**: one MR job if joining on a single column, **two** MR jobs if joining on two columns.
- The **rightmost table is buffered** — for best performance, make sure the **largest table is listed last (rightmost)**, so the smaller ones get buffered instead.
- **Minimize the data kept in memory** for better performance overall.
- Join happens **before** the `WHERE` clause is evaluated — the full join completes first, *then* filtering is applied.
- Hive can be hinted to **stream a specific table** rather than buffer it.

**Other Join Variants**
- **Cross / Cartesian Join** — every row of Table A combined with every row of Table B. Result columns = A's columns + B's columns; result rows = A's rows × B's rows. (Very expensive — use with caution.)
- **Natural Join** — an inner/outer join where the join condition is automatically an equality check on column(s) that **share the same name** in both tables.
- **Self-Join** — a table joined with itself (left and right side are the same table) — useful for hierarchical/comparative data (e.g., comparing employees to their managers within one table).
- **Left Semi Join** — an efficient way to implement `IN`/`EXISTS` subqueries.
  - Cannot select any columns from the right-side table (it's used only as a filter).
  - The right table is scanned only **until a match is found** (vs. `IN`/`EXISTS`, which scans the entire table).
  - Allows checks on **multiple joined columns**, which plain `IN`/`EXISTS` subqueries can't do.
  ```sql
  SELECT * FROM A LEFT SEMI JOIN B ON A.key = B.key;
  ```

---

## 12. Join Optimization Strategies

**Map-Side Join**
- Uses **only the Mapper** — no Reducer needed, making it much faster.
- Works when **all tables except one are small** (fit in memory).
- The small table is loaded into memory and distributed to every node using the **distributed cache**.
- ❌ Cannot perform a **full outer join**.
- Left/Right joins only work efficiently if the **smaller table is on the correct side** — practically, this means only **right outer joins** work efficiently this way (since the left table needs to be the small one).
- The small table is read only **once**.
- Eliminates the sort/shuffle/reduce stages entirely, which is *why* it's so much faster.

**Bucketed Map Join**
- Works when tables are **bucketed on the join column**, and the bucket count of one table is a **multiple** of the other's.
- Instead of fetching the entire table, only the **relevant buckets** needed for the join are fetched — much more efficient.
- **Most efficient** when both tables are bucketed *and* sorted on the join column with the **exact same number of buckets** — in this case it becomes a **Sort-Merge Join**.

**Cases Where Map-Side Join Won't Work**
- Union followed by a map join
- Map join followed by a union
- Map join followed by another join
- Map join followed by another map join

**Skewed Join** (for handling data skew — a few key values with disproportionately many rows)
```sql
SET hive.optimize.skewjoin = true;
SET hive.skewjoin.key = 500000;
SET hive.skewjoin.mapjoin.map.tasks = 10000;
SET hive.skewjoin.mapjoin.min.split = 33554432;
```
- At runtime, Hive detects keys with heavy skew, sets them aside temporarily in HDFS, and processes them in a **separate, faster follow-up map-join job** — instead of letting one overloaded reducer bottleneck the entire query.

**Skewed Table** (a related but distinct feature — defined at table creation)
```sql
CREATE TABLE T (c1 STRING, c2 STRING)
SKEWED BY (c1) ON ('x1', 'x2', 'x3');
```
- Values known in advance to be very frequent (`x1`, `x2`, `x3`) get **split into their own separate files** at creation time.
- Hive uses this info during query execution to **skip or include whole files** based on the filter — improving performance for queries touching those skewed values.

---

# PART 5 — File Formats

An important, practical decision in Hive — which format you store data in significantly affects performance, compression, and compatibility.

## 13. CSV (Comma-Separated Values)

- **Row-based** — each line = one row.
- Has a header row for column names.
- **Semi-structured only** — no support for hierarchical/relational data.
- Not fully standardized (delimiters can vary: comma, tab, etc.).

**Pros:** human-readable, easy to edit manually, universally supported, simple to parse, compact (headers written once).
**Cons:** flat data only, no column type distinction (everything is text), no standard way to represent binary data, ambiguity between NULL and empty/quoted values, poor support for special characters.

## 14. JSON

- Key-value pairs, **partially structured**, supports **hierarchical** data (like XML, but typically smaller/more compact).
- Natively supported by most web languages/tools.

**Pros:** supports nested/hierarchical structures well, widely supported serialization, handles lists of objects naturally, the standard format for NoSQL databases (MongoDB, Couchbase, Cosmos DB).
**Cons:** larger file size than binary formats, less efficient for large-scale analytical scans compared to columnar formats.

## 15. Parquet

- **Column-based** storage format (developed by Cloudera & Twitter, 2013) — optimized for datasets with many columns.
- Highly **compressible and splittable**.
- **Self-describing** — files are binary but contain metadata (column names, types, compression, basic stats) at the **end of the file**.
- Optimized for **Write Once, Read Many (WORM)** — slow to write, very fast to read, especially when only accessing a **subset of columns**.

**Pros:** projection pushdown (only reads needed columns → less disk I/O), self-describing schema, works outside HDFS too (e.g., on GlusterFS/NFS), just plain files (easy to move/backup), native Spark support, excellent compression (up to ~75% with e.g. Snappy), fastest for read-heavy workloads, great for data-warehouse-style aggregations, supports predicate pushdown too (filters applied before reading unnecessary data).
**Cons:** requires thinking carefully about schema/types upfront, weaker native support outside Spark, **immutable** — no in-place modification or schema evolution (only overwrite, or add new columns).

## 16. Avro

- **Row-based**, highly splittable, similar in spirit to Java Serialization (a data serialization system).
- **Schema stored in JSON**, actual **data stored in binary** — small file size, efficient.
- Strong **schema evolution** support — handles added fields, missing fields, and changed fields gracefully, so **old software can read new data and vice versa**.
- Great for **write-heavy workloads** (easy to append new rows).

**Pros:** language-neutral, self-describing (schema in the file header), fast serialization/deserialization, splittable and compressible, read/write schemas don't need to match exactly (supports adding fields independently), sync markers make it highly splittable, compressible (e.g., with Snappy).

## 17. ORC (Optimized Row Columnar)

- Can reduce file size by up to ~75% (e.g., 100GB → 25GB).
- Data is organized into **stripes** (default size: **250MB**) — large stripes enable efficient reads from HDFS.
- A **file footer** holds: list of stripes, row counts per stripe, each column's data type, and column-level aggregates (count, min, max, sum).
- A **postscript** at the very end holds compression parameters and the compressed footer's size.
- **Self-describing** — schema is included in the file (use the ORC file dump command to inspect it).
- Supports **indexes and bloom filters**, which allow skipping down to the **row-group level** (default: 10,000 rows) — e.g., skipping rows where `age > 100` is impossible, purely from min/max stats, even on unsorted data.
- Multiple split calculation strategies exist (padding to block boundaries, reading file tails directly for split pruning, or caching footer info in the Metastore) to optimize how work gets distributed.

**File Format Quick Comparison**

| Format | Storage | Best For | Schema Evolution |
|---|---|---|---|
| CSV | Row | Simplicity, human readability | ❌ None |
| JSON | Row (hierarchical) | Nested/semi-structured data, NoSQL | Flexible but not managed |
| Avro | Row | Write-heavy workloads, data interchange | ✅ Strong |
| Parquet | Column | Read-heavy analytics, aggregations | ❌ Limited (append columns only) |
| ORC | Column | Hive-native analytics, heavy compression | Some support via footer metadata |

---

# PART 6 — Analytical Functions

## 18. Window Functions

**What they are**
Window functions let you perform a calculation across a **"window" (set) of rows related to the current row**, without collapsing the result into a single row (unlike a normal aggregate + `GROUP BY`). They **add a new column** to the existing table rather than reducing the number of rows.

- **`ORDER BY`** (inside the window clause) — defines the order in which the calculation is done (e.g., for running totals, ranks).
- **`PARTITION BY`** — splits the data into smaller groups; the window function's calculation **resets** for each partition.

**Common Window Functions**

| Function | What it does |
|---|---|
| **`ROW_NUMBER()`** | Assigns a unique, sequential number to each row based on the `ORDER BY`. Resets to 1 at the start of each `PARTITION BY` group. |
| **`RANK()`** | Assigns a rank based on `ORDER BY`. Rows with equal values get the **same rank**, and the **next rank skips** ahead accordingly (e.g., two rows ranked 1 → next row is ranked 3, not 2). |
| **`DENSE_RANK()`** | Same as `RANK()`, but **no gaps** — the next rank after a tie is always the very next integer (e.g., two rows ranked 1 → next row is ranked 2). |
| **`NTILE(n)`** | Divides each partition into `n` roughly equal buckets (e.g., `NTILE(5)` splits data into quintiles/20% chunks) — useful for percentile-style bucketing. |
| **`LAG(col, n)`** | Looks **backward** — fetches a value from a **preceding** row (`n` rows back, default 1). The first row(s) will be `NULL` since there's nothing before them. |
| **`LEAD(col, n)`** | Looks **forward** — fetches a value from a **following** row (`n` rows ahead, default 1). The last row(s) will be `NULL`. |

> Example: `LAG(sales, 1) OVER (PARTITION BY store_id ORDER BY month)` gives you **last month's sales** on the same row as this month's — perfect for calculating month-over-month change.

---

## 19. User-Defined Functions (UDFs)

**What are they?**
Custom functions you write in **Java** when Hive's built-in functions aren't enough.

- The class is derived from Hive's `UDF` base class.
- Must implement a single method: **`evaluate()`** — this is where all your custom logic goes.
- The method's **signature must match** how you intend to call the function in HiveQL.
- ⚠️ Simple UDFs work only with **simple/primitive data types**, not complex ones (Array/Map/Struct) — those need a different type of UDF (a **GenericUDF**).

**Data Type Mapping (Java ↔ Hive)**
Hive uses special "Writable" wrapper classes internally (for efficient serialization), so each Hive type maps to a corresponding Java class:

| Hive Type | Java Writable Class |
|---|---|
| `INT` | `IntWritable` |
| `BIGINT` | `LongWritable` |
| `CHAR` | `HiveCharWritable` |
| `VARCHAR` | `HiveVarcharWritable` |

**Why "Writable" classes?**
This relates to **serialization**:
- **Serialization** — converting a Java object into bytes, for writing to disk.
- **Deserialization** — converting bytes read from disk back into a Java object.

**Registering a UDF in Hive**
```sql
-- 1. Package your logic into a JAR file
-- 2. Add the JAR to Hive's classpath
ADD JAR /jar/location/on/hdfs/myfunctions.jar;

-- 3. Register it as a temporary function
CREATE TEMPORARY FUNCTION my_function AS 'com.example.MyUDFClass';
```

---

# PART 7 — Performance Optimization

## 20. Tez — Execution Engine

**Apache Tez** is a client-side library that acts as an **alternative execution engine** to traditional MapReduce, used by both Hive and Pig, for faster processing via **DAG (Directed Acyclic Graph)** formation.

**Why plain MapReduce is slow for chained queries**
- The Mapper reads data, processes it into key-value pairs, and **writes them temporarily to local disk**.
- Grouped key-value pairs are sent to Reducers **over the network**.
- Reducers save incoming data to local disk again, and **wait** for all Mappers to finish.
- Once complete, the Reducer processes the full set of values for a key and writes the output — which may then be **replicated**.
- A single complex Hive query often becomes **multiple sequential MapReduce jobs**, each with this same read/write overhead — a lot of wasted I/O.

**How Tez optimizes this**
- **Skips DFS writes** by piping a Reducer's output **directly** into the next Mapper as input (no unnecessary disk round-trip).
- **Cascades multiple Reducers** together without intervening Mapper steps in between.
- **Reuses containers** across successive processing phases (avoids the overhead of spinning up new containers each time).
- Uses **pre-warmed containers** for optimal resource usage/startup time.

## 21. Other Key Optimization Techniques

- **Use Left Semi Join instead of `IN`/`EXISTS`** — more efficient (see §11).
- **Choose the right file format** — columnar formats (ORC, Parquet) for read-heavy analytical queries; row-based (Avro) for write-heavy workloads (see Part 5).
- **Compression** — Hive queries involve a lot of Disk/Network I/O, which compression reduces by shrinking data size. Most Hive data formats (especially text-based ones) compress well.
  - ⚠️ **Trade-off**: compression/decompression itself costs CPU — a classic space-vs-compute trade-off.
- **Partitioning** and **Bucketing** — covered in depth in Part 3; both reduce the amount of data scanned per query.
- **Vectorization** (introduced in Hive 0.13) — instead of processing scans/aggregations/filters/joins **one row at a time**, Vectorized execution processes them in **batches of 1,024 rows at once**, significantly improving execution time. Enabled via two configuration parameters.
- **Cost-Based Optimization (CBO)** — before final execution, Hive can optimize the logical/physical query plan based on **actual query cost** (not just fixed rules) — influencing decisions like join order, join type, and degree of parallelism. Enabled via specific config parameters set at the start of a query/session.
- **Parallel Execution** — Hadoop can run MapReduce jobs in parallel, and Hive queries automatically benefit from this in some cases. However, a single complex query is often broken into **multiple sequential MR jobs by default**, even when some stages don't actually depend on each other. Enabling the **parallel execution flag** lets Hive run those independent stages **simultaneously**, better utilizing spare cluster capacity and reducing total query time.
- **Skewed Tables & Skewed Joins** — see §12.

---

# PART 8 — Error Handling & Troubleshooting

## 22. Common Hive/Hadoop Errors & Fixes

**"Container memory requirement exceeds physical memory limits"**
This can come from three different sources of failure:

| Failure Source | Relevant Parameter | Fix |
|---|---|---|
| **Mapper failure** | `mapreduce.map.memory.mb` (memory limit), `mapreduce.map.java.opts` (heap size) | Increase both parameters. |
| **Reducer failure** | `mapreduce.reduce.memory.mb`, `mapreduce.reduce.java.opts` | Increase both parameters. |
| **ApplicationMaster failure** | `yarn.app.mapreduce.am.resource.mb`, `yarn.app.mapreduce.am.command-opts` | Increase both — and keep `command-opts` at roughly **80%** of `resource.mb`. |

**GC Overhead Limit Exceeded (JobHistory Server OOM)**
Usually happens when:
- The cluster's master node is too small (e.g., JobHistory server heap set to only 1GB).
- Jobs are very large (thousands of mapper tasks).

**Fix:** use a larger master node (≥60GB RAM), and increase the JobHistory server heap size (e.g., to 4GB or even 8GB for very large jobs).

**"No valid local directory" error (Mapper/Reducer failure)**
MapReduce stores intermediate data in local directories (`mapreduce.cluster.local.dir`). If none of these directories has enough free space, the job fails.

**Fix:**
- Ensure sufficient local disk space is available.
- Compress intermediate output to reduce space needs:
```sql
SET mapreduce.map.output.compress = true;
SET mapreduce.map.output.compress.codec = org.apache.hadoop.io.compress.SnappyCodec;
```

**Out of Memory Error with ORC files**
Often caused by the default ORC split strategy (`HYBRID`), which needs more memory.

**Fix:**
```sql
SET hive.exec.orc.split.strategy = BI;
```

**"Lock wait timeout exceeded" (Hive job fails during partitioned INSERT)**
This is a **MySQL transaction timeout** on the Hive Metastore backend, usually happening under heavy Metastore traffic (many concurrent partition inserts).

**Fix:** increase `innodb_lock_wait_timeout` on the MySQL side (default is 50 seconds) to give transactions more time before giving up.

---

# PART 9 — Bonus: Related Data Warehousing Concept

## 23. Slowly Changing Dimensions (SCD)

This term was flagged without a definition — it's a classic **data warehousing** concept, commonly taught alongside Hive since Hive is often used to build data warehouses.

**What is it?**
A **Slowly Changing Dimension** describes how to handle **changes to dimension data over time** (e.g., a customer's address changes, a product's category changes) in a data warehouse — since, unlike fast-changing transactional data, these changes happen *occasionally*, not constantly.

**The Common Types**
| Type | Behavior |
|---|---|
| **SCD Type 0** | The value **never changes** once set (e.g., a customer's original signup date). |
| **SCD Type 1** | **Overwrite** the old value with the new one — no history kept. Simple, but you lose the ability to see what the value used to be. |
| **SCD Type 2** | **Keep full history** — insert a **new row** for each change, typically with `effective_date`/`end_date` and/or an `is_current` flag. Most common approach when historical accuracy matters (e.g., for accurate historical reporting). |
| **SCD Type 3** | Keep **limited history** — add a new column (e.g., `previous_value`) to store just the prior value, alongside the current one. |

> Example (Type 2): A customer moves from "Delhi" to "Mumbai." Instead of overwriting the row, you'd insert a **new row** with `city = 'Mumbai'`, `effective_date = today`, and mark the old row's `end_date` = today, `is_current = false`. This way, any sales made *before* the move still correctly report against "Delhi" in historical analysis.

**How this connects to Hive:** since Hive tables are traditionally **append-friendly but not great at in-place updates** (especially with Parquet/ORC's immutability), SCD Type 2 (insert new rows + flag old ones) is a much more natural fit in Hive than SCD Type 1 (overwrite), which requires proper `MERGE`/ACID table support to do efficiently.

---

## Quick Recap Table

| Term | One-liner |
|---|---|
| Hive | SQL-like data warehouse layer on top of HDFS |
| Schema-on-Read | Schema applied only when data is queried, not when written |
| Metastore | Stores table/database metadata (schema, location, partitions) |
| Managed Table | Hive owns data + metadata; drop = data deleted |
| External Table | Only metadata in Hive; drop = data stays intact |
| Temporary Table | Session-scoped scratch table, auto-deleted after session |
| Partitioning | Splits table into HDFS directories by column value — filter faster |
| Bucketing | Hash-splits data into a fixed number of files — great for joins/sampling |
| Left Semi Join | Efficient IN/EXISTS alternative; can't select right-table columns |
| Map-Side Join | Join using only Mappers, small table cached in memory, no Reducer |
| Bucketed Map Join | Fetches only relevant buckets instead of full tables |
| Skewed Join/Table | Special handling for keys with disproportionately many rows |
| Parquet / ORC | Columnar formats — great for read-heavy analytics |
| Avro | Row-based, strong schema evolution — great for write-heavy loads |
| Window Function | Adds a calculated column over a set of related rows (no row reduction) |
| RANK vs DENSE_RANK | Ties skip ahead vs. ties stay consecutive |
| LAG / LEAD | Pull a value from a previous / following row |
| UDF | Custom Java function extending Hive's UDF class, via `evaluate()` |
| Tez | DAG-based execution engine, faster than plain MapReduce |
| Vectorization | Processes rows in batches of 1024 instead of one at a time |
| CBO | Optimizes query plan based on actual estimated cost |
| SCD | Strategy for handling changes to dimension data over time (Types 0–3) |

