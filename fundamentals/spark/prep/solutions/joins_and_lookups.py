from pyspark.sql import SparkSession
from pyspark.sql.connect.functions import row_number
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql.window import Window

# ============================================================
# Problem 5: Categorize products by price range: Budget, Mid-Range, Premium.
# Topic: when, otherwise Time: 15 min
# ============================================================

spark = SparkSession.builder.appName("when").master("local").getOrCreate()

data5 = [
    (1, "Widget A",  15.00),
    (2, "Widget B",  45.00),
    (3, "Widget C", 120.00),
    (4, "Widget D",  30.00),
    (5, "Widget E", 200.00),
    (6, "Widget F",   8.00),
]

schema5 = StructType([
    StructField("id", IntegerType()),
    StructField("product", StringType()),
    StructField("price", DoubleType())
])

df5 = spark.createDataFrame(data5, schema5)

category_df = df5.withColumn("category",
                            f.when(f.col("price") < f.lit(20), f.lit("Budget"))
                            .when(f.col("price") < f.lit(100), f.lit("Mid-Range"))
                            .otherwise(f.lit("Premium")))
category_df.show()


# ============================================================
# Problem 6: Find the top 3 highest-paid employees.
# Topic: Sort and Limit
# ============================================================

data6 = [
    (1, "Alice",   75000),
    (2, "Bob",     82000),
    (3, "Charlie", 68000),
    (4, "Diana",   95000),
    (5, "Eve",     71000),
    (6, "Frank",   88000),
]

schema6 = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
])

df6 = spark.createDataFrame(data6, schema6)

top_emp = df6.orderBy(f.col("salary").desc())
top_emp.show(3)
window_spec = Window.orderBy(f.col("salary").desc())

result_df = df6.withColumn("salary_rank", f.row_number().over(window_spec))
result_df.filter(f.col("salary_rank") <= f.lit(3)).show()

# ============================================================
# Problem 7: Remove duplicate customer records based on email address.
# Topic: dropDuplicates, distinct
# ============================================================
data7 = [
    (1, "Alice", "alice@example.com"),
    (2, "Bob",   "bob@example.com"),
    (3, "Alice", "alice@example.com"),  # duplicate
    (4, "Charlie", "charlie@example.com"),
    (5, "Bob",   "bob@example.com"),    # duplicate
]

schema7 = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
])

df7 = spark.createDataFrame(data7, schema7)
df7.dropDuplicates(["email"]).show()

# ============================================================
# Problem 8: Join employee data with department data to show employee names with department names.
# Topic: join, inner join
# ============================================================
employees = [
    (1, "Alice",   101),
    (2, "Bob",     102),
    (3, "Charlie", 101),
    (4, "Diana",   103),
]

departments = [
    (101, "Engineering"),
    (102, "Sales"),
    (103, "Marketing"),
]

emp_schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("dept_id", IntegerType()),
])

dept_schema = StructType([
    StructField("dept_id", IntegerType()),
    StructField("dept_name", StringType()),
])

emp_df = spark.createDataFrame(employees, emp_schema)
dept_df = spark.createDataFrame(departments, dept_schema)

# Task: Join to show emp_id, name, dept_name
# Expected:
# 1  Alice    Engineering
# 2  Bob      Sales
# 3  Charlie  Engineering
# 4  Diana    Marketing

result_df = emp_df.alias("emp").join(dept_df.alias("dept"), f.col("emp.dept_id") == f.col("dept.dept_id"),"inner")
result_df.select(f.col("emp.*"), f.col("dept.dept_name")).show()