from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window

def que_36(spark: SparkSession):
    # ============================================================
    # Problem 35: Inter-Event Time Calculation
    # - **Topics:** Window, lag, timestamp diff
    #
    # Calculate the time gap in minutes between consecutive user actions.
    # Expected:
    # +---+-----+---+--------+
    # | id| name|age|    city|
    # +---+-----+---+--------+
    # |  1|Alice| 30|New York|
    # |  2|  Bob| 25|  London|
    # +---+-----+---+--------+
    # ============================================================
    data = [
        (1, '{"name": "Alice", "age": 30, "city": "New York"}'),
        (2, '{"name": "Bob", "age": 25, "city": "London"}'),
    ]

    schema = StructType([
        StructField("id", IntegerType()),
        StructField("json_str", StringType())
    ])

    json_schema = StructType([
        StructField("name", StringType()),
        StructField("age", IntegerType()),
        StructField("city", StringType())

    ])

    df = spark.createDataFrame(data, schema)
    result = df.select(
        F.col("*"),
        F.from_json(F.col("json_str"), json_schema).alias("json_data")
    )

    result.select(
        F.col("id"),
        F.col("json_data.name"),
        F.col("json_data.age"),
        F.col("json_data.city")
    ).show()

def que_37(spark:SparkSession):
    # ============================================================
    # Problem 37: Extract from Complex Nested Structs
    # - **Topics:** Dot notation, struct manipulation
    #
    # Extract inner fields from a deeply nested DataFrame schema.
    # Expected:
    # +-----+-------------+-------+
    # | name|       street|zipcode|
    # +-----+-------------+-------+
    # |Alice|  123 Main St|  10001|
    # |  Bob|456 Market St|  94105|
    # +-----+-------------+-------+
    # ============================================================
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

    df = spark.createDataFrame(data, user_schema)

    df.printSchema()
    df.select(
        F.col('name'),
        F.col('address.street'),
        F.col('address.zipcode')
    ).show()

def que_38(spark:SparkSession):
    # ============================================================
    # Problem 38: Transform Arrays with Higher-Order Functions (`transform`)
    # - **Topics:** transform, lambda functions in Spark
    #
    # Multiply every element in an integer array column by 2 using Spark SQL higher-order functions.
    # +---+----------+
    # | id|doubled   |
    # +---+----------+
    # |  1|[2, 4, 6] |
    # |  2|[8, 10]   |
    # +---+----------+
    # ============================================================
    data = [
        (1, [1, 2, 3]),
        (2, [4, 5]),
    ]

    schema = StructType([
        StructField('id', IntegerType()),
        StructField('numbers', ArrayType(IntegerType()))
    ])

    df = spark.createDataFrame(data, schema)

    df.printSchema()
    df.show()

    df.select(
        F.col('id'),
        F.transform(F.col('numbers'), lambda x: x * 2).alias('numbers')
    ).show()

def que_39(spark:SparkSession):
    # ============================================================
    # Problem 39: Filter Arrays with Higher-Order Functions (`filter`)
    # - **Topics:** filter on arrays, lambda
    #
    # Filter an array column to keep only even numbers.
    # +---+----------+
    # | id|evens     |
    # +---+----------+
    # |  1|[2, 4]    |
    # |  2|[6, 8]    |
    # +---+----------+
    # ============================================================
    data = [
        (1, [1, 2, 3, 4]),
        (2, [5, 6, 7, 8]),
    ]

    schema = StructType([
        StructField('id', StringType()),
        StructField('numbers', ArrayType(IntegerType()))
    ])

    df = spark.createDataFrame(data, schema)
    df.printSchema()
    df.show()

    df.select(
        F.col('id'),
        F.filter(F.col('numbers'), lambda x: (x % 2) == 0).alias('evens')
    ).show()

def que_40(spark:SparkSession):
    # ============================================================
    # Problem 40: Explode Multiple Arrays (Zip/Parallel Explode)
    # - **Topics:** arrays_zip, explode
    #
    # You have two parallel arrays (`keys` and `values`). Explode them so they align correctly row-by-row.
    # +---+---+-----+
    # | id|key|value|
    # +---+---+-----+
    # |  1|  a|   10|
    # |  1|  b|   20|
    # |  2|  c|   30|
    # |  2|  d|   40|
    # |  2|  e|   50|
    # +---+---+-----+
    # ============================================================
    data = [
        (1, ["a", "b"], [10, 20]),
        (2, ["c", "d", "e"], [30, 40, 50]),
    ]

    schema = StructType([
        StructField('id', StringType()),
        StructField('keys', ArrayType(StringType())),
        StructField('values', ArrayType(IntegerType()))
    ])

    df = spark.createDataFrame(data, schema)
    result = df.select(
        F.col('id'),
        F.explode(F.arrays_zip(F.col('keys'), F.col('values'))).alias('zipped')
    ).select(
        F.col('ID'),
        F.col('zipped.keys'),
        F.col('zipped.values')
    )

    result.show()
    result.printSchema()


def main():
    spark = SparkSession.builder.appName('structures').master('local').getOrCreate()
    que_40(spark)



if __name__ == "__main__":
    main()
