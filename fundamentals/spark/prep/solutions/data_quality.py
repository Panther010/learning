from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f

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