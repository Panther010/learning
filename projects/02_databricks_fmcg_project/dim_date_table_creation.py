# Databricks notebook source
# MAGIC %md
# MAGIC **Import Required Libraries**

# COMMAND ----------

from pyspark.sql import functions as f

# COMMAND ----------

# MAGIC %md
# MAGIC **Define start and end dates**

# COMMAND ----------

# start date and end date
start_date = "2024-01-01"
end_date   = "2027-12-01"

# COMMAND ----------

# 1️⃣ Generate one row per month start between start_date and end_date
df = (
    spark.sql(f"""
        SELECT explode(
            sequence(
                to_date('{start_date}'),
                to_date('{end_date}'),
                interval 1 month
            )
        ) AS month_start_date
    """)
)


# 2️⃣ Add useful analytics columns
df = (
    df
    # Surrogate key at month grain
    .withColumn("date_key", f.date_format("month_start_date", "yyyyMM").cast("int"))
    .withColumn("year", f.year("month_start_date"))
    .withColumn("month_name", f.date_format("month_start_date", "MMMM"))
    .withColumn("month_short_name", f.date_format("month_start_date", "MMM"))
    .withColumn("quarter", f.concat(f.lit("Q"), f.quarter("month_start_date")))
    .withColumn("year_quarter", f.concat(f.col("year"), f.lit("-Q"), f.quarter("month_start_date")))
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select explode(sequence(to_date('2024-01-01'), to_date('2027-12-01'), interval 1 month)) as month_start_date

# COMMAND ----------

display(df)

# COMMAND ----------

# Save as a table
df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("fmcg.gold.dim_date")