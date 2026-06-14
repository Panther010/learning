from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("day2").master("local").getOrCreate()

#Problem 1: Filter and Count
#Difficulty: Easy Topics: DataFrame, filter, count Time: 10-15 min
#You have a dataset of customer orders. Filter to show only orders above $100 and count them.

data = [
    (1, "Alice", 85.50),
    (2, "Bob", 120.00),
    (3, "Charlie", 95.00),
    (4, "Diana", 210.00),
    (5, "Eve", 45.00),
    (6, "Frank", 150.00),
]

schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("amount", DoubleType())
])

df = spark.createDataFrame(data, schema)
df.show()

df = df.filter(f.col("amount") > f.lit(100))
df.show()



#Problem 2: Add Calculated Column
#Difficulty: Easy Topics: withColumn, expr Time: 10-15 min
#Add a new column showing order amount with 8% sales tax applied, rounded to 2 decimals.

prob2_data = [
    (1, "2026-01-15", 100.00),
    (2, "2026-02-20", 150.00),
    (3, "2026-03-10", 200.00),
    (4, "2026-01-25", 120.00),
]

prob2_schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product", StringType()),
    StructField("price", DoubleType()),
])

prob2_df = spark.createDataFrame(prob2_data, prob2_schema)
prob2_df.show()

prob2_df = prob2_df.withColumn("price_with_tax", (f.col("price") * f.lit(1.08)).cast("decimal(10,2)"))
prob2_df.show()



#Problem 3: GroupBy and Aggregate
#Difficulty: Easy Topics: groupBy, agg, sum, count Time: 15 min
#Group sales by salesperson and calculate total sales and order count for each.

prob3_data = [
    (1, "Alice",  500.00),
    (2, "Bob",    300.00),
    (3, "Alice",  700.00),
    (4, "Charlie",450.00),
    (5, "Bob",    250.00),
    (6, "Alice",  600.00),
    (7, "Charlie",800.00),
]

prob3_schema = StructType([
    StructField("sale_id", IntegerType()),
    StructField("salesperson", StringType()),
    StructField("amount", DoubleType()),
])

prob3_df = spark.createDataFrame(prob3_data, prob3_schema)

prob3_df = prob3_df.groupBy(f.col("salesperson")).agg(
    f.sum(f.col("amount")).alias("total_sales"),
    f.count(f.col("sale_id")).alias("order_count")).orderBy(
    f.col("total_sales").desc())

prob3_df.show()
