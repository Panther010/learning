from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f


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
# Task:
# 1. Calculate average salary (from non-null values)
# 2. Fill null salaries with this average
# 3. Remove rows where department is null
# Expected: 4 rows (Charlie removed), Bob and Eve have avg salary