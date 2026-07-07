from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as f
from pyspark.sql.window import Window
from datetime import datetime

spark = SparkSession.builder.appName("opt").master("local").getOrCreate()


# ============================================================
# Problem 26: Session Analysis (Time-Based Grouping)
# Topic: Window, lag, session detection
# Identify user sessions. A new session starts if more than 30 minutes have passed since the last event.
# Task:
# 1. Convert event_time to timestamp
# 2. For each user, calculate time difference from previous event
# 3. Mark session boundary when gap > 30 minutes
# 4. Assign session_id (cumulative sum of session boundaries)
# 5. Show user, event_time, session_id

# Expected:
# Alice has 2 sessions: [09:00-09:15], [10:00-10:05]
# Bob has 2 sessions: [09:05], [09:40-09:50]
# ============================================================

data26 = [
    ("Alice", "2026-06-08 09:00:00"),
    ("Alice", "2026-06-08 09:10:00"),  # same session
    ("Alice", "2026-06-08 09:15:00"),  # same session
    ("Alice", "2026-06-08 10:00:00"),  # new session (45 min gap)
    ("Alice", "2026-06-08 10:05:00"),  # same session
    ("Bob",   "2026-06-08 09:05:00"),
    ("Bob",   "2026-06-08 09:40:00"),  # new session (35 min gap)
    ("Bob",   "2026-06-08 09:50:00"),  # same session
]

schema26 = StructType([
    StructField("user", StringType()),
    StructField("event_time", StringType()),
])

df26 = spark.createDataFrame(data26, schema26)

df26_time = df26.select(
    f.col("user"),
    f.col("event_time").cast("timestamp"))

window_spec26 = Window.partitionBy(f.col("user")).orderBy("event_time")
df26_previous = df26_time.select(f.col("*"),
                                 f.lag("event_time").over(window_spec26).alias("previous_event"),
                                 f.timestamp_diff("MINUTE",
                                                  f.lag("event_time").over(window_spec26),
                                                  f.col("event_time")).alias("time_diff"))
df26_boundary = df26_previous.select(f.col("*"),
                                     f.when(
                                         ((f.col("time_diff").isNull()) |
                                          (f.col("time_diff") > f.lit(30))), f.lit(1))
                                     .otherwise(f.lit(0)).alias("is_new_session"))

df26_session = df26_boundary.select(f.col("*"),
                                    f.sum("is_new_session").over(window_spec26).alias("session_id"))

# final deliverable per task step 5
df26_final = df26_session.select("user", "event_time", "session_id")
df26_final.show()