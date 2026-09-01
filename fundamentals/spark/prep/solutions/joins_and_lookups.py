from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def que_5(spark: SparkSession):
    # ============================================================
    # Problem 5: Categorize products by price range: Budget, Mid-Range, Premium.
    # Topic: when, otherwise Time: 15 min
    # ============================================================

    data5 = [
        (1, "Widget A", 15.00),
        (2, "Widget B", 45.00),
        (3, "Widget C", 120.00),
        (4, "Widget D", 30.00),
        (5, "Widget E", 200.00),
        (6, "Widget F", 8.00),
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

def que_6(spark: SparkSession):
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

def que_7(spark: SparkSession):
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

def que_8(spark: SparkSession):
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

def que_41(spark: SparkSession):
    # ============================================================
    # Problem 41: Hierarchical Manager-Employee Path
    # - **Topics:** Self-joins, organizational hierarchies
    #
    # Find the direct manager and skip-level manager (manager's manager) for each employee.
    # Expected:
    # +-------+-------+------------------+
    # |name   |manager|skip_level_manager|
    # +-------+-------+------------------+
    # |Alice  |NULL   |NULL              |
    # |Bob    |Alice  |NULL              |
    # |Charlie|Bob    |Alice             |
    # +-------+-------+------------------+
    # ============================================================
    data = [
        (1, "Alice", None),
        (2, "Bob", 1),
        (3, "Charlie", 2),
    ]

    schema = StructType([
        StructField('emp_id', IntegerType()),
        StructField('name', StringType()),
        StructField('manager_id', IntegerType())
    ])

    df = spark.createDataFrame(data, schema)

    df.printSchema()
    df.show()

    df.alias('emp').join(df.alias('mgr'),
                         F.col('emp.manager_id') == F.col('mgr.emp_id'), 'left').join(
        df.alias('skip'), F.col('mgr.manager_id') == F.col('skip.emp_id'), 'left').select(
        F.col('emp.emp_id'),
        F.col('emp.name'),
        F.col('mgr.name').alias('manager'),
        F.col('skip.name').alias('skip_level_manager')
    ).show()

def que_42(spark: SparkSession):
    # ============================================================
    # Problem Problem 42: Finding Common Friends / Connections (Graph)
    # - **Topics:** Self-joins, graph relationships
    #
    # Given a table of friendships (User A is friends with User B), find mutual friends between pairs.
    # Expected:
    # +-------+-------+-------------+
    # |user_1 |user_2 |mutual_friend|
    # +-------+-------+-------------+
    # |Alice  |Bob    |Charlie      |
    # +-------+-------+-------------+
    # ============================================================
    data = [
        ("Alice", "Bob"),
        ("Bob", "Alice"),
        ("Alice", "Charlie"),
        ("Charlie", "Alice"),
        ("Bob", "Charlie"),
        ("Charlie", "Bob"),
    ]

    schema = StructType([
        StructField('user_a', StringType()),
        StructField('user_b', StringType())
    ])

    df = spark.createDataFrame(data, schema)

    df.printSchema()
    df.show()

    df.alias('a').join(df.alias('b'),
                       (F.col('a.user_b') == F.col('b.user_b')) &
                       (F.col('a.user_a') < F.col('b.user_a')) &
                       (F.col('b.user_a') < F.col('a.user_b')) ).select(
        F.col('a.user_a').alias('user_1'),
        F.col('b.user_a').alias('user_2'),
        F.col('a.user_b').alias('mutual_friend')).show()

def que_43(spark: SparkSession):
    # ============================================================
    # Problem 43: Interval Overlap Detection (Schedule Conflict)
    # - **Topics:** Non-equi joins, interval matching
    #
    # Find overlapping meeting room bookings.
    # Expected:
    # +-----------+-----------+
    # |booking_1  |booking_2  |
    # +-----------+-----------+
    # |          1|          2|
    # |          2|          1|
    # +-----------+-----------+
    # ============================================================
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

    df.printSchema()
    df.show()
    df.alias('a').join(df.alias('b'),
                       (F.col('a.booking_id') != F.col('b.booking_id')) &
                      ((F.col('a.end_time') > F.col('b.start_time')) &
                       (F.col('a.start_time') < F.col('b.end_time'))) |
                       ((F.col('a.start_time') < F.col('b.end_time')) &
                       (F.col('a.end_time') > F.col('b.end_time')))).select(
        F.col('a.booking_id').alias('booking_1'),
        F.col('b.booking_id').alias('booking_2')
    ).show()

def que_44(spark: SparkSession):
    # ============================================================
    # Problem 44: Running Balances with Deposits/Withdrawals
    # - **Difficulty:** Medium
    # - **Topics:** Window sums, transactions
    # - **Time:** 20-25 min
    #
    # Calculate bank account balances given mixed deposits (positive) and withdrawals (negative).
    # Expected:
    # +-------+----------+------+-------+
    # |account|      date|amount|balance|
    # +-------+----------+------+-------+
    # |  Alice|2026-06-01| 500.0|  500.0|
    # |  Alice|2026-06-02|-100.0|  400.0|
    # |  Alice|2026-06-03| 200.0|  600.0|
    # +-------+----------+------+-------+
    # ============================================================
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
    df.printSchema()
    df.show()
    win_spec = Window.partitionBy(F.col('account')).orderBy(F.col('date'))

    df.select(
        F.col('*'),
        F.sum(F.col('amount')).over(win_spec).alias('balance')
    ).show()

def que_45(spark: SparkSession):
    # ============================================================
    # Problem 45: Finding Gaps in Sequence Numbers
    # - **Topics:** Window lead, sequence analysis
    #
    # Find missing invoice numbers in a sequential list.
    #
    # Calculate bank account balances given mixed deposits (positive) and withdrawals (negative).
    # Expected:
    # +-------+----------+------+-------+
    # |account|      date|amount|balance|
    # +-------+----------+------+-------+
    # |  Alice|2026-06-01| 500.0|  500.0|
    # |  Alice|2026-06-02|-100.0|  400.0|
    # |  Alice|2026-06-03| 200.0|  600.0|
    # +-------+----------+------+-------+
    # ============================================================
    data = [
        (101,),
        (102,),
        (105,),  # Missing 103 and 104
        (106,),
    ]

    schema = StructType([StructField("invoice_id", IntegerType())])
    df = spark.createDataFrame(data, schema)

    df.show()
    df.printSchema()

    win_spec = Window.orderBy(F.col('invoice_id'))

    df.select(
        F.col('*'),
        F.lead(F.col('invoice_id')).over(win_spec).alias('next_num'),
        F.coalesce((F.lead(F.col('invoice_id')).over(win_spec) - F.col('invoice_id')), F.lit(0)).alias('num_diff')
    ).filter(F.col('num_diff') > F.lit(1)).select(
        (F.col('invoice_id') + 1).alias('missing_start'),
        (F.col('next_num') - 1).alias('missing_end')
    ).show()

def main():
    spark = SparkSession.builder.appName("when").master("local").getOrCreate()
    que_45(spark)


if __name__ == "__main__":
    main()