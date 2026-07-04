from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql.window import Window

spark = SparkSession.builder.appName("agg").master("local").getOrCreate()
# ============================================================
# Problem 15: You have a column with array values. Explode it so each array element becomes a separate row.
# Topic: explode, arrays
# Task: Explode skills array to create one row per skill
# Expected:
# 1  Alice    Python
# 1  Alice    SQL
# 1  Alice    Spark
# 2  Bob      Java
# 2  Bob      Scala
# ...
# ============================================================

data15 = [
    (1, "Alice",   ["Python", "SQL", "Spark"]),
    (2, "Bob",     ["Java", "Scala"]),
    (3, "Charlie", ["Python", "Java", "Scala", "SQL"]),
]

schema15 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("skills", ArrayType(StringType())),
])

df15 = spark.createDataFrame(data15, schema15)
df15.show()

df15.select(f.col("emp_id"), f.col("name"), f.explode(f.col("skills")).alias("skill")).show()

# ============================================================
# Problem 16: Find all pairs of employees who work in the same department (exclude pairing with self, avoid duplicates).
# Topic: self-join, alias
# Task: Find all unique pairs of employees in the same department
# Expected:
# Alice    Bob      Engineering
# Alice    Eve      Engineering
# Bob      Eve      Engineering
# Charlie  Diana    Sales

# Avoid:
# - Self-pairs (Alice-Alice)
# - Duplicate pairs (Alice-Bob and Bob-Alice counted once)
# ============================================================

data16 = [
    (1, "Alice",   "Engineering"),
    (2, "Bob",     "Engineering"),
    (3, "Charlie", "Sales"),
    (4, "Diana",   "Sales"),
    (5, "Eve",     "Engineering"),
]

schema16 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
])

df16 = spark.createDataFrame(data16, schema16)

df16.alias("emp1").join(df16.alias("emp2"),
                        ((f.col("emp1.department") == f.col("emp2.department")) &
                         (f.col("emp1.emp_id") < f.col("emp2.emp_id")))).select(
    f.col("emp1.name"), f.col("emp2.name"), f.col("emp1.department")).show()


# ============================================================
# Problem 17: For each employee's salary history, show previous salary, current salary, and next salary.
# Topic: Window, lead, lag
# Task: Add columns "prev_salary" and "next_salary" using lag() and lead()
# Expected for Alice 2025-01:
# prev_salary: 75000
# current:     80000
# next_salary: 85000
# ============================================================
data17 = [
    ("Alice", "2024-01", 70000),
    ("Alice", "2024-07", 75000),
    ("Alice", "2025-01", 80000),
    ("Alice", "2025-07", 85000),
    ("Bob",   "2024-01", 65000),
    ("Bob",   "2024-07", 68000),
    ("Bob",   "2025-01", 72000),
]

schema17 = StructType([
    StructField("name", StringType()),
    StructField("period", StringType()),
    StructField("salary", IntegerType()),
])

df17 = spark.createDataFrame(data17, schema17)
df17.show()
window_spec17 = Window.partitionBy(f.col("name")).orderBy(f.col("period"))
df17.select(f.col("*"),
            f.lag(f.col("salary")).over(window_spec17).alias("previous_salary"),
            f.lead(f.col("salary")).over(window_spec17).alias("next_salary")).show()


# ============================================================
# Problem 18: Find all customer emails that appear more than once in the dataset.
# Topic: groupBy, having, count
# Task: Show emails that appear more than once and their count
# Expected:
# alice@example.com     2
# bob@example.com       2
# ============================================================
data18 = [
    (1, "Alice", "alice@example.com"),
    (2, "Bob",   "bob@example.com"),
    (3, "Alice", "alice@example.com"),
    (4, "Charlie", "charlie@example.com"),
    (5, "Bob",   "bob@example.com"),
    (6, "Diana", "diana@example.com"),
]

schema18 = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
])

df18 = spark.createDataFrame(data18, schema18)
df18.show()
df18.groupBy(f.col("email")).agg(f.count(f.col("name")).alias("email_count")).filter(f.col("email_count") > f.lit(1)).show()

# ============================================================
# Problem 19: Combine two DataFrames and remove duplicates.
# Topic: union, dropDuplicates
# Task: Union df1 and df2, then remove duplicates
# Expected: 5 unique employees (Bob appears once)
# ============================================================
df1_data = [
    (1, "Alice", "Engineering"),
    (2, "Bob",   "Sales"),
    (3, "Charlie", "Marketing"),
]

df2_data = [
    (2, "Bob",   "Sales"),      # duplicate
    (4, "Diana", "Engineering"),
    (5, "Eve",   "Marketing"),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
])

df1 = spark.createDataFrame(df1_data, schema)
df2 = spark.createDataFrame(df2_data, schema)

df1.show()
df2.show()
df1.union(df2).dropDuplicates().show()
df1.union(df2).distinct().show()

# ============================================================
# Problem 20: Calculate month-over-month sales growth percentage for each product category.
# Topic: Window, lag, date functions
# Task: Calculate growth % = ((current - previous) / previous) * 100
# Round to 1 decimal. Show null for first month.
# Expected:
# Electronics 2026-01  10000  null
# Electronics 2026-02  12000  20.0%
# Electronics 2026-03  11000  -8.3%
# Clothing    2026-01   5000  null
# Clothing    2026-02   6000  20.0%
# Clothing    2026-03   7500  25.0%
# ============================================================
data20 = [
    ("Electronics", "2026-01", 10000),
    ("Electronics", "2026-02", 12000),
    ("Electronics", "2026-03", 11000),
    ("Clothing",    "2026-01",  5000),
    ("Clothing",    "2026-02",  6000),
    ("Clothing",    "2026-03",  7500),
]

schema20 = StructType([
    StructField("category", StringType()),
    StructField("month", StringType()),
    StructField("sales", IntegerType()),
])

df20 = spark.createDataFrame(data20, schema20)

df20.show()

