from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Create Spark Session
spark = SparkSession.builder.appName("Longest Non-UK Path").getOrCreate()

# Sample data
data = [
    (1, "UK", "FR"),
    (1, "FR", "US"),
    (1, "US", "CN"),
    (1, "CN", "UK"),
    (1, "UK", "DE"),
    (1, "DE", "UK"),
]

# Define schema and create DataFrame
columns = ["passengerId", "from", "to"]
df = spark.createDataFrame(data, schema=columns)
df.cache()
# Step 1: Retain the journey's sequence by adding an index
window_spec = Window.partitionBy("passengerId").orderBy(F.monotonically_increasing_id())
df_with_sequence = df.withColumn("seq", F.row_number().over(window_spec))
df_with_sequence.show()

# Step 2: Create a single journey list while retaining sequence
journey = (
    df_with_sequence.select(F.col("passengerId"), F.col("seq"), F.col("from").alias("country"))
    .union(
        df_with_sequence.select(F.col("passengerId"), (F.col("seq") + 0.5).alias("seq"), F.col("to").alias("country"))
    )
    .orderBy("passengerId", "seq")  # Ensure the journey sequence is maintained
)
journey.show()
# Step 3: Identify continuous non-UK segments
journey = journey.withColumn(
    "is_uk", F.when(F.col("country") == "UK", 1).otherwise(0)
)
journey.show()
journey = journey.withColumn(
    "group_id", F.sum("is_uk").over(Window.partitionBy("passengerId").orderBy("seq"))
)
journey.show()

# Step 4: Filter out UK entries and count distinct countries in each non-UK segment
non_uk_segments = (
    journey.filter(F.col("country") != "UK")
    .groupBy("passengerId", "group_id")
    .agg(F.countDistinct("country").alias("distinct_countries"))
)
non_uk_segments.show()
# Step 5: Find the maximum number of distinct countries per passenger
result = (
    non_uk_segments.groupBy("passengerId")
    .agg(F.max("distinct_countries").alias("max_countries"))
)

# Show result
result.show()
