import re
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def que_9(spark:SparkSession):
    # ============================================================
    # Problem 9: Replace null values in the salary column with the average salary, and filter out rows where department is null.
    # Topic: fillna, na.fill, isNull
    # Task:
    # 1. Calculate average salary (from non-null values)
    # 2. Fill null salaries with this average
    # 3. Remove rows where department is null
    # Expected: 4 rows (Charlie removed), Bob and Eve have avg salary
    # ============================================================

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

def que_10(spark:SparkSession):
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

def que_11(spark:SparkSession):
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

def que_12(spark:SparkSession):
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

def que_13(spark:SparkSession):
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

def que_14(spark:SparkSession):
    # ============================================================
    # Problem 14: Pivot sales data so each product category becomes a column showing total sales per region.
    # Topic: pivot, groupBy
    # Task: Pivot to show:
    # region  Electronics  Clothing
    # North      8000        3000
    # South      7000        2000
    # East       6000        4000
    # ============================================================

    data14 = [
        ("North", "Electronics", 5000),
        ("North", "Clothing",    3000),
        ("South", "Electronics", 7000),
        ("South", "Clothing",    2000),
        ("East",  "Electronics", 6000),
        ("East",  "Clothing",    4000),
        ("North", "Electronics", 3000),
    ]

    schema14 = StructType([
        StructField("region", StringType()),
        StructField("category", StringType()),
        StructField("sales", IntegerType()),
    ])

    df14 = spark.createDataFrame(data14, schema14)

    df14.show()

    result_df14 = df14.groupBy(f.col("region")).pivot("category").agg(f.sum(f.col("sales")))
    result_df14.show()

def que_31(spark:SparkSession):
    # ============================================================
    # Problem 31: Moving Average Calculation
    # - **Topics:** Window, rowsBetween, average
    #
    # Calculate a 3-period moving average of stock prices (current row and 2 preceding rows).
    # Expected:
    # +------+----------+-----+------------+
    # |ticker|      date|price|moving_avg  |
    # +------+----------+-----+------------+
    # |  AAPL|2026-06-01|150.0|      150.00|
    # |  AAPL|2026-06-02|155.0|      152.50|
    # |  AAPL|2026-06-03|152.0|      152.33|
    # |  AAPL|2026-06-04|160.0|      155.67|
    # |  AAPL|2026-06-05|158.0|      156.67|
    # +------+----------+-----+------------+
    # ============================================================
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

    window_speac = Window.orderBy(F.col('date')).rowsBetween(-2, 0)
    df.withColumn(
       'moving_avg',
       F.round(F.avg(F.col('price')).over(window_speac), 2)
    ).show()

def que_32(spark:SparkSession):
    # ============================================================
    # Problem 32: Consecutive Logins (Gaps and Islands)
    # - **Topics:** Window, row_number, date arithmetic
    #
    # Find users who logged in for 3 or more consecutive days.
    # Expected:
    # +-----+------------------+
    # |user |consecutive_days  |
    # +-----+------------------+
    # |Alice|                3 |
    # +-----+------------------+
    # ============================================================
    data = [
        ("Alice", "2026-06-01"),
        ("Alice", "2026-06-02"),
        ("Alice", "2026-06-03"),  # 3 days streak
        ("Alice", "2026-06-06"),
        ("Bob", "2026-06-01"),
        ("Bob", "2026-06-03"),  # break in streak
        ("Bob", "2026-06-04"),
    ]

    schema = StructType([
        StructField("user", StringType()),
        StructField("login_date", StringType())
    ])

    df = spark.createDataFrame(data, schema)
    df.show()
    df.printSchema()

    win_spec = Window.partitionBy(F.col('user')).orderBy(F.col('login_date'))

    (df.select(
        F.col('*'),
        F.row_number().over(win_spec).alias('rn'),
        F.dateadd(F.col('login_date'), F.row_number().over(win_spec) * F.lit(-1)).alias('base_date')
    ).groupby(F.col('user'), F.col('base_date'))
    .agg(F.count(F.col('login_date')).alias('consecutive_days'))
    .filter(F.col('consecutive_days') >= F.lit(3))
     .show())

def que_33(spark:SparkSession):
    # ============================================================
    # Problem 33: First and Last Value in Window
    # - **Topics:** Window, first, last
    #
    # For each transaction log, show the first and last amount recorded for that customer across all their transactions.
    # Expected:
    # +------+--------+------+----------+------------+-----------+
    # |txn_id|customer|amount|      date|first_amount|last_amount|
    # +------+--------+------+----------+------------+-----------+
    # |     1|   Alice|  50.0|2026-06-01|        50.0|      150.0|
    # |     2|   Alice| 100.0|2026-06-03|        50.0|      150.0|
    # |     3|   Alice| 150.0|2026-06-05|        50.0|      150.0|
    # |     4|     Bob| 200.0|2026-06-02|       200.0|      250.0|
    # |     5|     Bob| 250.0|2026-06-04|       200.0|      250.0|
    # +------+--------+------+----------+------------+-----------+
    # ============================================================
    data = [
        (1, "Alice", 50.0, "2026-06-01"),
        (2, "Alice", 100.0, "2026-06-03"),
        (3, "Alice", 150.0, "2026-06-05"),
        (4, "Bob", 200.0, "2026-06-02"),
        (5, "Bob", 250.0, "2026-06-04"),
    ]

    schema = StructType([
        StructField("txn_id", IntegerType()),
        StructField("customer", StringType()),
        StructField("amount", DoubleType()),
        StructField("date", StringType()),
    ])

    df = spark.createDataFrame(data, schema)
    df.show()
    df.printSchema()

    win_spec = (Window.partitionBy(F.col('customer'))
                .orderBy(F.col('date'))
                .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing))

    df.select(
        F.col('*'),
        F.first(F.col('amount')).over(win_spec).alias('first_amount'),
        F.last(F.col('amount')).over(win_spec).alias('last_amount')
    ).show()

def que_34(spark: SparkSession):
    # ============================================================
    # Problem 34: Time-Windowed Retention Analysis
    # - **Difficulty:** Hard
    #
    # Calculate day-1 retention: Users who logged in on Day N and also logged in on Day N+1.
    # Expected:
    # +----------+------------+----------------+
    # |base_date |total_users |retained_users  |
    # +----------+------------+----------------+
    # |2026-06-01|           2|               1|
    # |2026-06-02|           1|               1|
    # +----------+------------+----------------+
    # ============================================================
    data = [
        ("Alice", "2026-06-01"),
        ("Alice", "2026-06-02"),  # Retained
        ("Bob", "2026-06-01"),
        ("Charlie", "2026-06-02"),
        ("Charlie", "2026-06-03"),  # Retained
    ]

    schema = StructType([
        StructField("user", StringType()),
        StructField("date", StringType()),
    ])

    df = spark.createDataFrame(data, schema)
    df.show()
    df.printSchema()

    win_spec = Window.partitionBy(F.col('user')).orderBy('date')
    df_with_base = df.select(
        F.col('*'),
        F.dateadd(F.col('date') ,(F.row_number().over(win_spec) - 1) * -1).alias('base_date'))
    df_with_base.show()

    streak_win = Window.partitionBy("user", "base_date")
    df_with_counts = df_with_base.withColumn("streak_days", F.count("date").over(streak_win))
    df_with_counts.show()

    (df_with_counts
     .groupby(F.col('base_date'))
     .agg(
        F.count_distinct('user').alias('total_users'),
        F.count_distinct(F.when(F.col('streak_days') > F.lit(1), F.col('user')).otherwise(F.lit(None))).alias('retained_users')
    ).show())

def que_35(spark: SparkSession):
    # ============================================================
    # Problem 35: Inter-Event Time Calculation
    # - **Topics:** Window, lag, timestamp diff
    #
    # Calculate the time gap in minutes between consecutive user actions.
    # Expected:
    # +-----+-------------------+-------------------+
    # |user |action_time        |minutes_since_last |
    # +-----+-------------------+-------------------+
    # |Alice|2026-06-01 10:00:00|               NULL|
    # |Alice|2026-06-01 10:15:00|               15.0|
    # |Alice|2026-06-01 10:45:00|               30.0|
    # +-----+-------------------+-------------------+
    # ============================================================
    data = [
        ("Alice", "2026-06-01 10:00:00"),
        ("Alice", "2026-06-01 10:15:00"),
        ("Alice", "2026-06-01 10:45:00"),
    ]

    schema = StructType([
        StructField("user", StringType()),
        StructField("action_time", StringType()),
    ])

    win_spec = Window.partitionBy(F.col('user')).orderBy(F.col('action_time'))

    df = spark.createDataFrame(data, schema)
    df.select(
        F.col('*'),
        F.timestamp_diff("MINUTE", F.lag(F.col('action_time'), 1).over(win_spec), F.col('action_time')).alias('minutes_since_last')
    ).show()


def main():
    spark = SparkSession.builder.appName("window").master("local").getOrCreate()
    que_35(spark)

if __name__ == '__main__':
    main()