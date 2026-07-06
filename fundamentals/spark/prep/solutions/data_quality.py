from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("dq").master("local").getOrCreate()

# ============================================================
# Problem Problem 21: Complex Filter with Multiple Conditions
# Topic: filter, and/or logic
# Task: Filter transactions where:
# (amount > 100 AND channel = "Online") OR (amount > 150 AND channel = "Store")
# Expected: 3 transactions (Alice Online, Charlie Online, Eve Store)
# ============================================================

data21 = [
    (1, "Alice",   "2026-01-15", 150.00, "Online"),
    (2, "Bob",     "2026-01-20", 80.00,  "Store"),
    (3, "Charlie", "2026-02-01", 200.00, "Online"),
    (4, "Diana",   "2026-02-10", 50.00,  "Online"),
    (5, "Eve",     "2026-03-05", 170.00, "Store"),
]

schema21 = StructType([
    StructField("txn_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("date", StringType()),
    StructField("amount", DoubleType()),
    StructField("channel", StringType()),
])

df21 = spark.createDataFrame(data21, schema21)

df21.show()
df21.filter(((f.col("amount") > f.lit(100)) & (f.col("channel") == f.lit("Online"))) |
            ((f.col("amount") > f.lit(150)) & (f.col("channel") == f.lit("Store")))).show()

# ============================================================
# Problem Problem 22: Calculate the 25th, 50th (median), and 75th percentile of salaries.
# Topic: approx_percentile, aggregate functions
# Task: Calculate 25th, 50th, 75th percentile of salary
# Use approx_percentile or percentile_approx
# ============================================================

data22 = [
    (1, "Alice",   75000),
    (2, "Bob",     82000),
    (3, "Charlie", 68000),
    (4, "Diana",   95000),
    (5, "Eve",     71000),
    (6, "Frank",   88000),
    (7, "Grace",   79000),
    (8, "Henry",   84000),
]

schema22 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
])

df22 = spark.createDataFrame(data22, schema22)

df22.show()

df22.agg(f.percentile_approx(f.col("salary"), [0.25, 0.5, 0.75]).alias("salary_percentile")).show(truncate=False)

# ============================================================
# Problem Problem 23: Join a large transactions table with a small lookup table using broadcast join.
# Topic: broadcast join, optimization
# Task: Join with broadcast hint on products table
# Show txn_id, product_name, amount
# ============================================================

# Large table (transactions)
transactions = [
    (1, 101, 150.00),
    (2, 102, 200.00),
    (3, 101, 180.00),
    (4, 103, 220.00),
    (5, 102, 160.00),
] * 1000  # Simulate large dataset

# Small table (products)
products = [
    (101, "Laptop"),
    (102, "Mouse"),
    (103, "Keyboard"),
]

txn_schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("amount", DoubleType()),
])

prod_schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
])

txn_df = spark.createDataFrame(transactions, txn_schema)
prod_df = spark.createDataFrame(products, prod_schema)

txn_df.show()
prod_df.show()

txn_df.alias("txn").join(f.broadcast(prod_df).alias("prod"), f.col("txn.product_id") == f.col("prod.product_id"), "inner").show()

# ============================================================
# Problem Problem 24: Aggregate Multiple Columns
# Topic: agg, multiple aggregations
# Task: Group by department, show:
# - employee_count
# - total_salary
# - avg_salary (rounded to 2 decimals)
# - min_salary
# - max_salary
# ============================================================

data24 = [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 88000),
    (3, "Charlie", "Sales",       75000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Engineering", 92000),
    (6, "Frank",   "Sales",       78000),
]

schema24 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df24 = spark.createDataFrame(data24, schema24)
df24.show()

df24.groupBy(f.col("department")).agg(
    f.count(f.col("emp_id")).alias("employee_count"),
    f.sum(f.col("salary")).alias("total_salary"),
    f.avg(f.col("salary")).alias("avg_salary"),
    f.min(f.col("salary")).alias("min_salary"),
    f.max(f.col("salary")).alias("max_salary")
).show()

# ============================================================
# Problem Problem 25: Cumulative Distribution
# Topic: Window, cume_dist
# Task: Add column "percentile_rank" showing cumulative distribution
# Use cume_dist() window function
# Expected: Charlie (68k) at ~0.167, Diana (95k) at 1.0
# ============================================================
data25 = [
    (1, "Alice",   75000),
    (2, "Bob",     82000),
    (3, "Charlie", 68000),
    (4, "Diana",   95000),
    (5, "Eve",     71000),
    (6, "Frank",   88000),
]

schema25 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
])

df25 = spark.createDataFrame(data25, schema25)

df25.show()

window_spec_25 =  Window.orderBy(f.col("salary"))
df25.select(f.col("*"),
            f.cume_dist().over(window_spec_25).alias("percentile_rank")).show()