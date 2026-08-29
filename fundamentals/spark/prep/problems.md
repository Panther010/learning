# PySpark Advanced Problem Bank (Problems 31–60)

---

## Category 1: Advanced Window & Time-Series (Problems 31–35)

### Problem 31: Moving Average Calculation
- **Difficulty:** Medium-Hard
- **Topics:** Window, rowsBetween, average
- **Time:** 20-25 min

Calculate a 3-period moving average of stock prices (current row and 2 preceding rows).

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, avg, round

spark = SparkSession.builder.appName("problem31").master("local[*]").getOrCreate()

data = [
    ("AAPL", "2026-06-01", 150.0),
    ("AAPL", "2026-06-02", 155.0),
    ("AAPL", "2026-06-03", 152.0),
    ("AAPL", "2026-06-04", 160.0),
    ("AAPL", "2026-06-05", 158.0),
]

schema = StructType([
    StructField("ticker", StringType()),
    StructField("date", StringType()),
    StructField("price", DoubleType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Compute a 3-row moving average of `price` per `ticker`, ordered by `date`. Round to 2 decimal places.

**Expected Output Validation:**
```
+------+----------+-----+------------+
|ticker|      date|price|moving_avg  |
+------+----------+-----+------------+
|  AAPL|2026-06-01|150.0|      150.00|
|  AAPL|2026-06-02|155.0|      152.50|
|  AAPL|2026-06-03|152.0|      152.33|
|  AAPL|2026-06-04|160.0|      155.67|
|  AAPL|2026-06-05|158.0|      156.67|
+------+----------+-----+------------+
```

---

### Problem 32: Consecutive Logins (Gaps and Islands)
- **Difficulty:** Hard
- **Topics:** Window, row_number, date arithmetic
- **Time:** 35-40 min

Find users who logged in for 3 or more consecutive days.

```python
data = [
    ("Alice", "2026-06-01"),
    ("Alice", "2026-06-02"),
    ("Alice", "2026-06-03"),  # 3 days streak
    ("Alice", "2026-06-06"),
    ("Bob",   "2026-06-01"),
    ("Bob",   "2026-06-03"),  # break in streak
    ("Bob",   "2026-06-04"),
]

schema = StructType([
    StructField("user", StringType()),
    StructField("login_date", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Identify user streaks of consecutive login dates. Group by user and streak group to find users with ≥3 consecutive days.

**Expected Output Validation:**
```
+-----+------------------+
|user |consecutive_days  |
+-----+------------------+
|Alice|                3 |
+-----+------------------+
```

---

### Problem 33: First and Last Value in Window
- **Difficulty:** Medium
- **Topics:** Window, first, last
- **Time:** 20 min

For each transaction log, show the first and last amount recorded for that customer across all their transactions.

```python
data = [
    (1, "Alice", 50.0,  "2026-06-01"),
    (2, "Alice", 100.0, "2026-06-03"),
    (3, "Alice", 150.0, "2026-06-05"),
    (4, "Bob",   200.0, "2026-06-02"),
    (5, "Bob",   250.0, "2026-06-04"),
]

schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("amount", DoubleType()),
    StructField("date", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Add columns `first_amount` and `last_amount` for each customer based on chronological order.

**Expected Output Validation:**
```
+------+--------+------+----------+------------+-----------+
|txn_id|customer|amount|      date|first_amount|last_amount|
+------+--------+------+----------+------------+-----------+
|     1|   Alice|  50.0|2026-06-01|        50.0|      150.0|
|     2|   Alice| 100.0|2026-06-03|        50.0|      150.0|
|     3|   Alice| 150.0|2026-06-05|        50.0|      150.0|
|     4|     Bob| 200.0|2026-06-02|       200.0|      250.0|
|     5|     Bob| 250.0|2026-06-04|       200.0|      250.0|
+------+--------+------+----------+------------+-----------+
```

---

### Problem 34: Time-Windowed Retention Analysis
- **Difficulty:** Hard
- **Topics:** Self-join on conditions, conditional aggregation
- **Time:** 35 min

Calculate day-1 retention: Users who logged in on Day N and also logged in on Day N+1.

```python
data = [
    ("Alice", "2026-06-01"),
    ("Alice", "2026-06-02"),  # Retained
    ("Bob",   "2026-06-01"),
    ("Charlie","2026-06-02"),
    ("Charlie","2026-06-03"), # Retained
]

schema = StructType([
    StructField("user", StringType()),
    StructField("date", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Find the retention rate (retained users / total users on base date).

**Expected Output Validation:**
```
+----------+------------+----------------+
|base_date |total_users |retained_users  |
+----------+------------+----------------+
|2026-06-01|           2|               1|
|2026-06-02|           1|               1|
+----------+------------+----------------+
```

---

### Problem 35: Inter-Event Time Calculation
- **Difficulty:** Medium
- **Topics:** Window, lag, timestamp diff
- **Time:** 20-25 min

Calculate the time gap in minutes between consecutive user actions.

```python
data = [
    ("Alice", "2026-06-01 10:00:00"),
    ("Alice", "2026-06-01 10:15:00"),
    ("Alice", "2026-06-01 10:45:00"),
]

schema = StructType([
    StructField("user", StringType()),
    StructField("action_time", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Find the minutes elapsed since the user's previous action using `lag()`.

**Expected Output Validation:**
```
+-----+-------------------+-------------------+
|user |action_time        |minutes_since_last |
+-----+-------------------+-------------------+
|Alice|2026-06-01 10:00:00|               NULL|
|Alice|2026-06-01 10:15:00|               15.0|
|Alice|2026-06-01 10:45:00|               30.0|
+-----+-------------------+-------------------+
```

---

## Category 2: Advanced Structs & JSON Parsing (Problems 36–40)

### Problem 36: Parse Nested JSON String
- **Difficulty:** Medium
- **Topics:** from_json, schema definition
- **Time:** 20-25 min

Parse a string column containing JSON data into structured DataFrame columns.

```python
data = [
    (1, '{"name": "Alice", "age": 30, "city": "New York"}'),
    (2, '{"name": "Bob", "age": 25, "city": "London"}'),
]

schema = StructType([
    StructField("id", IntegerType()),
    StructField("json_str", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Define a JSON schema matching the fields (`name`, `age`, `city`), parse `json_str`, and flatten the resulting struct columns.

**Expected Output Validation:**
```
+---+-----+---+--------+
| id| name|age|    city|
+---+-----+---+--------+
|  1|Alice| 30|New York|
|  2|  Bob| 25|  London|
+---+-----+---+--------+
```

---

### Problem 37: Extract from Complex Nested Structs
- **Difficulty:** Medium
- **Topics:** Dot notation, struct manipulation
- **Time:** 15-20 min

Extract inner fields from a deeply nested DataFrame schema.

```python
inner_schema = StructType([
    StructField("street", StringType()),
    StructField("zipcode", StringType())
])
user_schema = StructType([
    StructField("name", StringType()),
    StructField("address", inner_schema)
])

data = [
    ("Alice", ("123 Main St", "10001")),
    ("Bob", ("456 Market St", "94105")),
]

df = spark.createDataFrame(data, StructType([
    StructField("name", StringType()),
    StructField("info", user_schema)
]))
```

**Task:** Extract `street` and `zipcode` into top-level columns.

**Expected Output Validation:**
```
+-----+-------------+-------+
| name|       street|zipcode|
+-----+-------------+-------+
|Alice|  123 Main St|  10001|
|  Bob|456 Market St|  94105|
+-----+-------------+-------+
```

---

### Problem 38: Transform Arrays with Higher-Order Functions (`transform`)
- **Difficulty:** Hard
- **Topics:** transform, lambda functions in Spark
- **Time:** 25-30 min

Multiply every element in an integer array column by 2 using Spark SQL higher-order functions.

```python
data = [
    (1, [1, 2, 3]),
    (2, [4, 5]),
]

schema = StructType([
    StructField("id", IntegerType()),
    StructField("numbers", ArrayType(IntegerType())),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Use `transform(col("numbers"), lambda x: x * 2)` to double each element.

**Expected Output Validation:**
```
+---+----------+
| id|doubled   |
+---+----------+
|  1|[2, 4, 6] |
|  2|[8, 10]   |
+---+----------+
```

---

### Problem 39: Filter Arrays with Higher-Order Functions (`filter`)
- **Difficulty:** Hard
- **Topics:** filter on arrays, lambda
- **Time:** 25 min

Filter an array column to keep only even numbers.

```python
data = [
    (1, [1, 2, 3, 4]),
    (2, [5, 6, 7, 8]),
]

schema = StructType([
    StructField("id", IntegerType()),
    StructField("numbers", ArrayType(IntegerType())),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Keep only even numbers inside the array using `filter()`.

**Expected Output Validation:**
```
+---+----------+
| id|evens     |
+---+----------+
|  1|[2, 4]    |
|  2|[6, 8]    |
+---+----------+
```

---

### Problem 40: Explode Multiple Arrays (Zip/Parallel Explode)
- **Difficulty:** Hard
- **Topics:** arrays_zip, explode
- **Time:** 30 min

You have two parallel arrays (`keys` and `values`). Explode them so they align correctly row-by-row.

```python
data = [
    (1, ["a", "b"], [10, 20]),
    (2, ["c", "d", "e"], [30, 40, 50]),
]

schema = StructType([
    StructField("id", IntegerType()),
    StructField("keys", ArrayType(StringType())),
    StructField("values", ArrayType(IntegerType())),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Use `arrays_zip` combined with `explode` to map keys to their corresponding values.

**Expected Output Validation:**
```
+---+---+-----+
| id|key|value|
+---+---+-----+
|  1|  a|   10|
|  1|  b|   20|
|  2|  c|   30|
|  2|  d|   40|
|  2|  e|   50|
+---+---+-----+
```

---

## Category 3: Graph & Recursive/Relational Patterns (Problems 41–45)

### Problem 41: Hierarchical Manager-Employee Path
- **Difficulty:** Hard
- **Topics:** Self-joins, organizational hierarchies
- **Time:** 35 min

Find the direct manager and skip-level manager (manager's manager) for each employee.

```python
data = [
    (1, "Alice", None),
    (2, "Bob", 1),
    (3, "Charlie", 2),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("manager_id", IntegerType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Perform multiple self-joins to output `emp_name`, `manager_name`, and `skip_level_manager_name`.

**Expected Output Validation:**
```
+-------+-------+------------------+
|name   |manager|skip_level_manager|
+-------+-------+------------------+
|Alice  |NULL   |NULL              |
|Bob    |Alice  |NULL              |
|Charlie|Bob    |Alice             |
+-------+-------+------------------+
```

---

### Problem 42: Finding Common Friends / Connections (Graph)
- **Difficulty:** Hard
- **Topics:** Self-joins, graph relationships
- **Time:** 35-40 min

Given a table of friendships (User A is friends with User B), find mutual friends between pairs.

```python
data = [
    ("Alice", "Bob"),
    ("Bob", "Alice"),
    ("Alice", "Charlie"),
    ("Charlie", "Alice"),
    ("Bob", "Charlie"),
    ("Charlie", "Bob"),
]

schema = StructType([
    StructField("user_a", StringType()),
    StructField("user_b", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Find pairs of users who have at least one common friend.

**Expected Output Validation:**
```
+-------+-------+-------------+
|user_1 |user_2 |mutual_friend|
+-------+-------+-------------+
|Alice  |Bob    |Charlie      |
+-------+-------+-------------+
```

---

### Problem 43: Interval Overlap Detection (Schedule Conflict)
- **Difficulty:** Hard
- **Topics:** Non-equi joins, interval matching
- **Time:** 35 min

Find overlapping meeting room bookings.

```python
data = [
    (1, "Room A", "10:00", "11:00"),
    (2, "Room A", "10:30", "11:30"),  # Overlaps with booking 1
    (3, "Room A", "12:00", "13:00"),  # No overlap
]

schema = StructType([
    StructField("booking_id", IntegerType()),
    StructField("room", StringType()),
    StructField("start_time", StringType()),
    StructField("end_time", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Self-join on `room` where `start_1 < end_2` and `end_1 > start_2` (excluding self-match).

**Expected Output Validation:**
```
+-----------+-----------+
|booking_1  |booking_2  |
+-----------+-----------+
|          1|          2|
|          2|          1|
+-----------+-----------+
```

---

### Problem 44: Running Balances with Deposits/Withdrawals
- **Difficulty:** Medium
- **Topics:** Window sums, transactions
- **Time:** 20-25 min

Calculate bank account balances given mixed deposits (positive) and withdrawals (negative).

```python
data = [
    ("Alice", "2026-06-01", 500.0),
    ("Alice", "2026-06-02", -100.0),
    ("Alice", "2026-06-03", 200.0),
]

schema = StructType([
    StructField("account", StringType()),
    StructField("date", StringType()),
    StructField("amount", DoubleType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Compute cumulative balance over time per account.

**Expected Output Validation:**
```
+-------+----------+------+-------+
|account|      date|amount|balance|
+-------+----------+------+-------+
|  Alice|2026-06-01| 500.0|  500.0|
|  Alice|2026-06-02|-100.0|  400.0|
|  Alice|2026-06-03| 200.0|  600.0|
+-------+----------+------+-------+
```

---

### Problem 45: Finding Gaps in Sequence Numbers
- **Difficulty:** Hard
- **Topics:** Window lead, sequence analysis
- **Time:** 30 min

Find missing invoice numbers in a sequential list.

```python
data = [
    (101,),
    (102,),
    (105,),  # Missing 103 and 104
    (106,),
]

schema = StructType([StructField("invoice_id", IntegerType())])
df = spark.createDataFrame(data, schema)
```

**Task:** Use `lead()` to find gaps between consecutive invoice IDs.

**Expected Output Validation:**
```
+-------------+-------------+
|missing_start|  missing_end|
+-------------+-------------+
|          103|          104|
+-------------+-------------+
```

---

## Category 4: Performance Tuning, Partitioning & Join Strategies (Problems 46–50)

### Problem 46: Managing Shuffle Partitions
- **Difficulty:** Medium
- **Topics:** spark.sql.shuffle.partitions, repartitioning
- **Time:** 15 min

Demonstrate how to control partition counts prior to heavy aggregations.

```python
data = [(i, f"cat_{i%5}", float(i)) for i in range(1000)]
df = spark.createDataFrame(data, ["id", "category", "val"])
```

**Task:** Check current partition count using `df.rdd.getNumPartitions()`, then optimize shuffle performance by repartitioning by `category` into 4 partitions before running a `groupBy`.

**Expected Output Validation:** Partition count on grouped output should match 4.

---

### Problem 47: Bucketing Tables for Optimized Joins
- **Difficulty:** Hard
- **Topics:** saveAsTable, bucketing concept
- **Time:** 25 min

Write a simulation of bucketing two tables by a common join key to avoid shuffle joins.

```python
# Conceptual practice script framework
df1 = spark.createDataFrame([(1, "A"), (2, "B")], ["id", "val1"])
df2 = spark.createDataFrame([(1, "X"), (2, "Y")], ["id", "val2"])
```

**Task:** Write out code syntax using `.bucketBy(4, "id").sortBy("id").saveAsTable(...)` for a managed warehouse table. (Verify syntax and explain shuffle reduction.)

---

### Problem 48: Avoiding OOM with `coalesce` vs `repartition`
- **Difficulty:** Medium
- **Topics:** coalesce, partition reduction
- **Time:** 15 min

Reduce the number of output files written to disk after a filter operation without causing a full shuffle.

```python
df = spark.range(10000).repartition(20)
```

**Task:** Reduce partitions from 20 down to 2 using `coalesce()` and save/verify.

**Expected Output Validation:** Output partition count equals 2 without full shuffle overhead.

---

### Problem 49: Broadcast Hash Join Enforcement
- **Difficulty:** Medium
- **Topics:** broadcast(), hint syntax
- **Time:** 15 min

Force Spark to execute a broadcast join on a non-trivial dataset when the Catalyst optimizer fails to pick it automatically.

```python
large_df = spark.range(100000).withColumn("val", col("id") * 2)
small_df = spark.createDataFrame([(i, f"name_{i}") for i in range(5)], ["id", "name"])
```

**Task:** Join `large_df` and `small_df` explicitly using `broadcast(small_df)`. Inspect the execution plan via `.explain()` to verify `BroadcastHashJoin` is used.

---

### Problem 50: Handling Data Skew with Custom Salting
- **Difficulty:** Hard
- **Topics:** Salting keys, join optimization
- **Time:** 40 min

Resolve a severe performance bottleneck caused by a hot key (NULL or high-frequency key) during a join.

```python
# Hot key scenario: 90% of rows have id = 0
keys = [0] * 90 + [1, 2, 3, 4, 5, 6, 7, 8, 9]
data_large = [(k, f"data_{i}") for i, k in enumerate(keys)]
data_small = [(i, f"lookup_{i}") for i in range(10)]

df_large = spark.createDataFrame(data_large, ["id", "val"])
df_small = spark.createDataFrame(data_small, ["id", "desc"])
```

**Task:** Implement salting on `df_large` (e.g., append a random integer 0-4 to `id`) and replicate rows in `df_small` across 5 salt variants, then join.

---

## Category 5: Complex Aggregations & Cube/Rollup (Problems 51–55)

### Problem 51: Multi-Dimensional Rollup Summary
- **Difficulty:** Medium-Hard
- **Topics:** rollup, hierarchical aggregations
- **Time:** 25 min

Calculate total revenue grouped by country, state, and overall total using `rollup`.

```python
data = [
    ("USA", "California", 100),
    ("USA", "California", 150),
    ("USA", "New York", 200),
    ("Canada", "Ontario", 300),
]

schema = StructType([
    StructField("country", StringType()),
    StructField("state", StringType()),
    StructField("sales", IntegerType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Run `df.rollup("country", "state").sum("sales")`.

**Expected Output Validation:** Includes subtotals for each state/country combination, country-level totals, and a grand total row (`country=null`, `state=null`).

---

### Problem 52: Full Cube Combinations
- **Difficulty:** Hard
- **Topics:** cube aggregation
- **Time:** 25 min

Generate all possible combinations of aggregates across multiple dimensions using `cube`.

```python
data = [
    ("Electronics", "Online", 1000),
    ("Clothing", "Store", 500),
]

df = spark.createDataFrame(data, ["category", "channel", "sales"])
```

**Task:** Use `cube("category", "channel")` to compute sales totals across all cross-sections.

**Expected Output Validation:** Produces 2² = 4 grouping combinations (Detail, Category total, Channel total, Grand total).

---

### Problem 53: Conditional Grouping (`agg` with `filter`)
- **Difficulty:** Medium
- **Topics:** Conditional counts, sum(when(...))
- **Time:** 20 min

Count the number of active vs. inactive users per department in a single aggregation pass.

```python
data = [
    ("Eng", True),
    ("Eng", False),
    ("Eng", True),
    ("Sales", False),
]

df = spark.createDataFrame(data, ["department", "is_active"])
```

**Task:** Group by department and count active and inactive users separately using `sum(when(...))`.

**Expected Output Validation:**
```
+----------+------------+--------------+
|department|active_count|inactive_count|
+----------+------------+--------------+
|       Eng|           2|             1|
|     Sales|           0|             1|
+----------+------------+--------------+
```

---

### Problem 54: Weighted Average Calculation
- **Difficulty:** Medium
- **Topics:** Aggregation, expression formulas
- **Time:** 20 min

Calculate the weighted average score per student.

```python
data = [
    ("Alice", 80, 0.3),
    ("Alice", 90, 0.7),
    ("Bob", 70, 0.5),
    ("Bob", 80, 0.5),
]

df = spark.createDataFrame(data, ["student", "score", "weight"])
```

**Task:** Compute weighted average: `∑(score×weight) / ∑(weight)` per student.

**Expected Output Validation:**
```
+-------+-----------------+
|student|weighted_average |
+-------+-----------------+
|  Alice|             87.0|
|    Bob|             75.0|
+-------+-----------------+
```

---

### Problem 55: Median Calculation via `expr`
- **Difficulty:** Medium
- **Topics:** percentile_approx, median
- **Time:** 20 min

Find the exact or approximate median salary across departments.

```python
data = [
    ("Eng", 70000),
    ("Eng", 80000),
    ("Eng", 120000),
]

df = spark.createDataFrame(data, ["department", "salary"])
```

**Task:** Group by department and find the 50th percentile using `percentile_approx`.

---

## Category 6: Data Quality, Validation & Custom Operations (Problems 56–60)

### Problem 56: Automated Null Value Profiling
- **Difficulty:** Medium
- **Topics:** Dynamic DataFrame aggregation, null checks
- **Time:** 25 min

Write a reusable snippet that counts null values across all columns of a DataFrame automatically.

```python
data = [(1, "Alice", None), (None, None, 50.0)]
df = spark.createDataFrame(data, ["id", "name", "score"])
```

**Task:** Programmatically build an aggregation expression list using list comprehensions (`[count(when(col(c).isNull(), c)).alias(c) for c in df.columns]`) and run it.

**Expected Output Validation:**
```
+--------+-----------+------------+
|id_nulls|name_nulls |score_nulls |
+--------+-----------+------------+
|       1|          1|           1|
+--------+-----------+------------+
```

---

### Problem 57: Outlier Detection using IQR (Interquartile Range)
- **Difficulty:** Hard
- **Topics:** percentile_approx, outlier filtering
- **Time:** 35 min

Filter out outlier rows where values fall below `Q1 − 1.5×IQR` or above `Q3 + 1.5×IQR`.

```python
data = [(i, float(i * 10)) for i in range(10)] + [(1, 1000.0)]  # 1000 is an outlier
df = spark.createDataFrame(data, ["id", "value"])
```

**Task:** Calculate Q1 (25th percentile) and Q3 (75th percentile) via `approx_percentile`, compute IQR, and filter out the outlier row.

---

### Problem 58: Schema Enforcement & Bad Record Quarantine
- **Difficulty:** Hard
- **Topics:** Corrupt record handling (_corrupt_record), parsing safety
- **Time:** 30 min

Handle malformed JSON strings without crashing the Spark job.

```python
data = [
    ('{"id": 1, "name": "Alice"}',),
    ('INVALID_JSON_STRING',),
]
df = spark.createDataFrame(data, ["json_col"])
```

**Task:** Parse the JSON string with a schema that includes a `_corrupt_record` column field to safely separate valid rows from bad rows.

---

### Problem 59: Deduplication with Priority Ordering (Window Dedup)
- **Difficulty:** Hard
- **Topics:** Window, row_number, custom preference sorting
- **Time:** 30 min

Deduplicate customer records where a customer has multiple emails, keeping only the most recently updated record.

```python
data = [
    (1, "alice@old.com", "2026-01-01"),
    (1, "alice@new.com", "2026-06-01"),  # Keep this (latest date)
]

schema = StructType([
    StructField("customer_id", IntegerType()),
    StructField("email", StringType()),
    StructField("updated_at", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Use a window function partitioned by `customer_id` ordered by `updated_at DESC` to assign row numbers, then filter for `row_num == 1`.

---

### Problem 60: Slowly Changing Dimension (SCD Type 2) Simulation
- **Difficulty:** Hard
- **Topics:** Window functions, effective date tracking
- **Time:** 40 min

Generate valid `effective_start_date` and `effective_end_date` bounds for records that change over time.

```python
data = [
    (1, "Alice", "New York", "2026-01-01"),
    (1, "Alice", "Boston",   "2026-04-01"),
    (1, "Alice", "Seattle",  "2026-06-01"),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("city", StringType()),
    StructField("change_date", StringType()),
])

df = spark.createDataFrame(data, schema)
```

**Task:** Use `lead()` to assign an `effective_end_date` to each record (setting the current/latest record's end date to a high date like `"9999-12-31"`).

**Expected Output Validation:**
```
+-------+-----+--------+---------------------+-------------------+
| emp_id| name|    city|effective_start_date|effective_end_date|
+-------+-----+--------+---------------------+-------------------+
|      1|Alice|New York|2026-01-01           |2026-04-01         |
|      1|Alice|  Boston|2026-04-01           |2026-06-01         |
|      1|Alice| Seattle|2026-06-01           |9999-12-31         |
+-------+-----+--------+---------------------+-------------------+
```

---

## What's Next

Which specific category or problem would you like to tackle first, or do you need a deep dive into the solution pattern for any of these advanced windows or optimizations?
