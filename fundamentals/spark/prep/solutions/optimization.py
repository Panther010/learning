from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql.window import Window
from datetime import datetime

spark = SparkSession.builder.appName("opt").master("local").getOrCreate()


# ============================================================
# Problem 26: Session Analysis (Time-Based Grouping)
# Topic: Window, lag, session detection
# Identify user sessions. A new session starts if more than 30 minutes have passed since the last event.
# Task:
# 1. Convert event_time to timestamp
# 2. For each user, calculate time difference from previous event
# 3. Mark session boundary when gap > 30 minutes
# 4. Assign session_id (cumulative sum of session boundaries)
# 5. Show user, event_time, session_id

# Expected:
# Alice has 2 sessions: [09:00-09:15], [10:00-10:05]
# Bob has 2 sessions: [09:05], [09:40-09:50]
# ============================================================

data26 = [
    ("Alice", "2026-06-08 09:00:00"),
    ("Alice", "2026-06-08 09:10:00"),  # same session
    ("Alice", "2026-06-08 09:15:00"),  # same session
    ("Alice", "2026-06-08 10:00:00"),  # new session (45 min gap)
    ("Alice", "2026-06-08 10:05:00"),  # same session
    ("Bob",   "2026-06-08 09:05:00"),
    ("Bob",   "2026-06-08 09:40:00"),  # new session (35 min gap)
    ("Bob",   "2026-06-08 09:50:00"),  # same session
]

schema26 = StructType([
    StructField("user", StringType()),
    StructField("event_time", StringType()),
])

df26 = spark.createDataFrame(data26, schema26)

df26_time = df26.select(
    f.col("user"),
    f.col("event_time").cast("timestamp"))

window_spec26 = Window.partitionBy(f.col("user")).orderBy("event_time")
df26_previous = df26_time.select(f.col("*"),
                                 f.lag("event_time").over(window_spec26).alias("previous_event"),
                                 f.timestamp_diff("MINUTE",
                                                  f.lag("event_time").over(window_spec26),
                                                  f.col("event_time")).alias("time_diff"))
df26_boundary = df26_previous.select(f.col("*"),
                                     f.when(
                                         ((f.col("time_diff").isNull()) |
                                          (f.col("time_diff") > f.lit(30))), f.lit(1))
                                     .otherwise(f.lit(0)).alias("is_new_session"))

df26_session = df26_boundary.select(f.col("*"),
                                    f.sum("is_new_session").over(window_spec26).alias("session_id"))

# final deliverable per task step 5
df26_final = df26_session.select("user", "event_time", "session_id")
df26_final.show()



# ============================================================
# Problem 27: Top N Per Group with Ties
# Difficulty: Hard Topics: Window, dense_rank, filter
# Find top 2 salaries in each department, but include ties (use dense_rank instead of rank).
# Task: Show top 2 salaries per department (include ties)
# Expected Engineering: Alice, Bob (both rank 1), Charlie (rank 2) = 3 rows
# Expected Sales: Diana, Eve (both rank 1), Frank (rank 2) = 3 rows
# ============================================================

data27= [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 95000),  # tie for 1st
    (3, "Charlie", "Engineering", 88000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Sales",       82000),  # tie for 1st
    (6, "Frank",   "Sales",       78000),
    (7, "Grace",   "Sales",       75000),
]

schema27 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df27 = spark.createDataFrame(data27, schema27)

df27.show()

window_spec27 = Window.partitionBy(f.col("department")).orderBy(f.col("salary").desc())

df27.select(f.col("*"), f.dense_rank().over(window_spec27).alias("rn")).filter(f.col("rn") <= f.lit(2)).show()


# ============================================================
# Problem 28: Skewed Join Optimization
# Difficulty: Hard Topics: salting, skew handling
# Handle a highly skewed join where one key has disproportionately many records.
# Task: Implement salting to distribute product_id=101 across partitions
# Steps:
# 1. Add salt column (random 0-9) to large_df
# 2. Replicate small_df 10 times with salt values 0-9
# 3. Join on (product_id, salt)
# 4. Remove salt column from result
# ============================================================

# Skewed large table (80% of records have product_id = 101)
large_data = [(i, 101, 100.0) for i in range(1, 801)] + \
             [(i, 102, 150.0) for i in range(801, 901)] + \
             [(i, 103, 200.0) for i in range(901, 1001)]

# Small dimension table
small_data = [
    (101, "Laptop"),
    (102, "Mouse"),
    (103, "Keyboard"),
]

large_schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("amount", DoubleType()),
])

small_schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
])

large_df = spark.createDataFrame(large_data, large_schema)
small_df = spark.createDataFrame(small_data, small_schema)

large_df_salted = large_df.withColumn("salt", f.floor(f.rand() * 10))

salt_df = spark.createDataFrame([(i,) for i in range(10)], ["salt"])

small_df_salted = small_df.crossJoin(salt_df)

joined_df = large_df_salted.join(small_df_salted, on=["product_id", "salt"], how="inner")

final_df = joined_df.drop("salt")
final_df.show(5)
print(f"Total rows after salted join: {final_df.count()}")

# ============================================================
# Problem 29: Complex Multi-Level Aggregation
# Difficulty: Hard Topics: groupBy, rollup, cube
# Calculate sales totals at multiple levels: by region, by category, by region+category, and grand total.
# Task: Use rollup or cube to show:
# 1. Total by region and category
# 2. Total by region (all categories)
# 3. Total by category (all regions)
# 4. Grand total (all regions, all categories)

# Expected output includes rows like:
# North  Electronics   5000   (detail)
# North  null          8000   (region total)
# null   Electronics  18000   (category total)
# null   null         27000   (grand total)
# Hint: Use rollup("region", "category") or cube("region", "category")
# rollup(region, category) only produces hierarchical subtotals in the order given:
#       (region, category) → (region, null) → (null, null).
#       It will never produce (null, category) — a category-only subtotal skipping region —
#       because rollup assumes region is the "outer" grouping level and category is nested inside it.
# cube(region, category) produces every combination of grouping/ungrouping:
#       (region,category), (region,null), (null,category), (null,null) — all 2² = 4 combinations.
# ============================================================

data29 = [
    ("North", "Electronics", 5000),
    ("North", "Clothing",    3000),
    ("South", "Electronics", 7000),
    ("South", "Clothing",    2000),
    ("East",  "Electronics", 6000),
    ("East",  "Clothing",    4000),
]

schema29 = StructType([
    StructField("region", StringType()),
    StructField("category", StringType()),
    StructField("sales", IntegerType()),
])

df29 = spark.createDataFrame(data29, schema29)

df29.cube(f.col("region"), f.col("category")).agg(
    f.sum(f.col("sales")).alias("sales"),
    f.grouping_id("region", "category").alias("grouping_level")
).withColumn(
    "level",
    f.when(f.col("grouping_level") == f.lit(0), f.lit("Detail"))
    .when(f.col("grouping_level") == f.lit(1), f.lit("Region Total"))
    .when(f.col("grouping_level") == f.lit(2), f.lit("Category Total"))
    .when(f.col("grouping_level") == f.lit(3), f.lit("Grand Total"))
).orderBy(f.col("region").asc_nulls_last(), f.col("category").asc_nulls_last()).show()

rollup_region = (
    df29.rollup(f.col("region"), f.col("category"))
    .agg(
        f.sum("sales").alias("sales"),
        f.grouping_id("region", "category").alias("grouping_level")
    )
).show()


"""
# ============================================================
# Problem 30: Incremental Processing Pattern
# Difficulty: Window, checkpoint, watermark concepts Time: 40-45 min
# Process only new records since last run (simulate incremental batch processing).
# Task:
# 1. Filter records with date > last_processed_date
# 2. Calculate daily totals for these new records
# 3. Join with historical aggregates to get cumulative totals
# 4. Update checkpoint to new max date

# This simulates an incremental ETL pattern where you only process
# new data and merge with existing aggregates
# ============================================================"""

# Full dataset
full_data30 = [
    (1, "Alice",  "2026-06-01", 100.0),
    (2, "Bob",    "2026-06-02", 150.0),
    (3, "Charlie","2026-06-03", 200.0),
    (4, "Diana",  "2026-06-04", 120.0),
    (5, "Eve",    "2026-06-05", 180.0),
    (6, "Frank",  "2026-06-06", 210.0),
]

schema30 = StructType([
    StructField("txn_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("date", StringType()),
    StructField("amount", DoubleType()),
])

df30 = spark.createDataFrame(full_data30, schema30)

# Simulate: last processed date was 2026-06-03
last_processed_date = "2026-06-03"

df30.show()