import re
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql.window import Window

# ============================================================
# Problem 9: Replace null values in the salary column with the average salary, and filter out rows where department is null.
# Topic: fillna, na.fill, isNull
# Task:
# 1. Calculate average salary (from non-null values)
# 2. Fill null salaries with this average
# 3. Remove rows where department is null
# Expected: 4 rows (Charlie removed), Bob and Eve have avg salary
# ============================================================

spark = SparkSession.builder.appName("window").master("local").getOrCreate()

data9 = [
    (1, "Alice",   75000, "Engineering"),
    (2, "Bob",     None,  "Sales"),
    (3, "Charlie", 68000, None),
    (4, "Diana",   95000, "Engineering"),
    (5, "Eve",     None,  "Marketing"),
]

schema9 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
    StructField("department", StringType()),
])

df9 = spark.createDataFrame(data9, schema9)
avg_salary = df9.select(f.avg(f.col("salary"))).first()[0]

df_filled = df9.fillna({'salary': avg_salary})
df_filled.show()

df_result = df_filled.dropna(subset=['department'])
df_result.show()

# ============================================================
# Problem 10: Rename columns to follow snake_case convention and select only relevant columns.
# Topic: withColumnRenamed, select, alias
# Task:
# Task: Rename to: emp_id, emp_name, dept_name, annual_salary
# Select only: emp_id, emp_name, annual_salary
# ============================================================

data10 = [
    (1, "Alice", "Engineering", 75000),
    (2, "Bob", "Sales", 82000),
]

schema10 = StructType([
    StructField("EmployeeID", IntegerType()),
    StructField("EmployeeName", StringType()),
    StructField("DepartmentName", StringType()),
    StructField("AnnualSalary", IntegerType()),
])

df10 = spark.createDataFrame(data10, schema10)
df_select = df10.select(f.col("EmployeeID").alias("emp_id"),
                        f.col("EmployeeName").alias("emp_name"),
                        f.col("DepartmentName").alias("dept_name"),
                        f.col("AnnualSalary").alias("annual_salary"))
df_select.select(f.col("emp_id"), f.col("emp_name"), f.col("annual_salary")).show()

def camel_to_snake(name: str) -> str:
    # Adds an underscore before any capital letter and converts to lowercase
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
df_select2 = df10.select([f.col(c).alias(camel_to_snake(c)) for c in df10.columns])
df_select2.show()

# ============================================================
# Problem 11: Rank employees by salary within each department. Show rank, employee name, department, salary.
# Topic: Rank Within Groups
# Task: Add a "rank" column showing rank by salary within each department
# (highest salary = rank 1)
# Expected:
# Engineering: Alice(1), Eve(2), Bob(3)
# Sales: Diana(1), Frank(2), Charlie(3)
# Marketing: Grace(1)
# ============================================================

data11 = [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 88000),
    (3, "Charlie", "Sales",       75000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Engineering", 92000),
    (6, "Frank",   "Sales",       78000),
    (7, "Grace",   "Marketing",   85000),
]

schema11 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df11 = spark.createDataFrame(data11, schema11)
df11.show()

window_spec = Window.partitionBy(f.col("department")).orderBy(f.col("salary").desc())
df11_result = df11.select(f.col("*"), f.rank().over(window_spec).alias("rank"))
df11_result.show()

# ============================================================
# Problem 12: Calculate running total of sales for each salesperson ordered by date.
# Topic: Window functions, sum, rowsBetween
# Task: Add "running_total" column
# Expected for Alice:
# 2026-01-10  500.00   running_total: 500.00
# 2026-01-15  300.00   running_total: 800.00
# 2026-01-20  450.00   running_total: 1250.00
# ============================================================
data12 = [
    ("Alice", "2026-01-10", 500.00),
    ("Alice", "2026-01-15", 300.00),
    ("Alice", "2026-01-20", 450.00),
    ("Bob",   "2026-01-12", 600.00),
    ("Bob",   "2026-01-18", 200.00),
    ("Bob",   "2026-01-22", 350.00),
]

schema12 = StructType([
    StructField("salesperson", StringType()),
    StructField("sale_date", StringType()),
    StructField("amount", DoubleType()),
])

df12 = spark.createDataFrame(data12, schema12)

df12.show()
window_spec12 = Window.partitionBy(f.col("salesperson")).orderBy(f.col("sale_date"))
df_result12 = df12.select(f.col("*"), f.sum(f.col("amount")).over(window_spec12).alias("running_total"))
df_result12.show()

# ============================================================
# Problem 13: For each department, find the employee with the highest salary (return full row, not just the max value).
# Topic: Window functions, max, filter
# Task: Return the highest-paid employee in each department
# Expected:
# Engineering: Alice  95000
# Sales:       Diana  82000
# Marketing:   Eve    85000
# ============================================================

data13 = [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 88000),
    (3, "Charlie", "Sales",       75000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Marketing",   85000),
]

schema13 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df13 = spark.createDataFrame(data13, schema13)

df13.show()
window_spec13 = Window.partitionBy(f.col("department")).orderBy(f.col("salary").desc())
df13.select(f.col("*"), f.rank().over(window_spec13).alias("max_salary")).filter(f.col("max_salary") == f.lit(1)).drop(f.col("max_salary")).show()