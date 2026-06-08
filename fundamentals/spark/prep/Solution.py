from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("sol").master("local").getOrCreate()

# Sales data
sales_data = [
 (1, "Alice", "Electronics", 1200.0, "2026-01-15"),
 (2, "Bob", "Clothing", 350.0, "2026-01-20"),
 (3, "Alice", "Electronics", 850.0, "2026-02-01"),
 (4, "Charlie", "Electronics", 2200.0, "2026-02-14"),
 (5, "Bob", "Electronics", 975.0, "2026-02-20"),
 (6, "Alice", "Clothing", 420.0, "2026-03-05"),
 (7, "Charlie", "Clothing", 180.0, "2026-03-10"),
 (8, "Diana", "Electronics", 3100.0, "2026-03-15"),
 (9, "Diana", "Clothing", 290.0, "2026-03-22"),
 (10,"Bob", "Electronics", 1540.0, "2026-03-28"),
]

# id salesperson category amount sale_date
schema = StructType([
 StructField("id", IntegerType()),
 StructField("salesperson", StringType()),
 StructField("category", StringType()),
 StructField("amount", DoubleType()),
 StructField("sale_date", StringType())
])

df = spark.createDataFrame(sales_data, schema)
df.show()


# Task: Filter the dataframe to show only Electronics rows
# Expected: 6 rows
df.filter(f.lower(f.col("category")) == f.lit("electronics")).show()

# Task: Add a new column "amount_with_tax"
# Tax rate is 20% — amount_with_tax = amount * 1.20
# Round to 2 decimal places
df.withColumn("amount_with_tax", f.col("amount") * f.lit(1.20)).show()


# Task: Group by salesperson, sum the amount, order by total descending
# Expected output:
# Diana 3390.0
# Charlie 2380.0
# Bob 2865.0
# Alice 2470.0
df.groupBy(f.col("salesperson")).agg(f.sum("amount").alias("total_amount")).orderBy(f.col("total_amount").desc()).show()


# Task:
# 1. Convert sale_date column from StringType to DateType
# 2. Add a new column "month" extracting the month number
# 3. Show id, salesperson, amount, sale_date, month
# Task: Group by category AND month, sum amount
# You'll need the month column from Problem 4
# Order by month, then category
# Expected:
# Electronics Jan 2050.0
# Clothing Jan 350.0
# Electronics Feb 4025.0
# ... etc



# Task: Add column "sale_tier" based on amount:
# amount >= 2000 → "High"
# amount >= 1000 → "Medium"
# amount < 1000 → "Low"
# Task: For each salesperson return the row with their maximum sale
# (return the full row, not just the max value)
# Hint: there are two ways — Window function or groupBy + join
# Expected:
# Alice Electronics 1200.0
# Bob Electronics 1540.0
# Charlie Electronics 2200.0
# Diana Electronics 3100.0


# Task: Add a column "running_total" showing cumulative sales
# for each salesperson ordered by sale_date
# Expected for Alice:
# 2026-01-15 1200.0 running_total: 1200.0
# 2026-02-01 850.0 running_total: 2050.0
# 2026-03-05 420.0 running_total: 2470.0


# Task: Pivot the data so each category becomes a column
# showing total sales per salesperson per category
# Expected:
# salesperson Clothing Electronics
# Alice 420.0 2050.0
# Bob 350.0 2515.0
# Charlie 180.0 2200.0
# Diana 290.0 3100.0


# Task: For each category, calculate month-over-month growth %
# growth % = ((this_month - last_month) / last_month) * 100
# Round to 1 decimal place. Show null for first month (no previous)
# Expected:
# Electronics Jan 2050.0 null
# Electronics Feb 4025.0 +96.3%
# Electronics Mar 4615.0 +14.7%
# Clothing Jan 350.0 null
# Clothing Feb 0.0 -100%
# Clothing Mar 890.0 null (or handle div by zero)