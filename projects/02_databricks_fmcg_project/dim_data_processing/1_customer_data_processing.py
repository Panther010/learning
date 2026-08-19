# Databricks notebook source
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %run /Workspace/Users/bakulseth001@gmail.com/fmcg_project/utilities

# COMMAND ----------

dbutils.widgets.text("catalog", "fmcg", "Catalog")
dbutils.widgets.text("data_source", "customers", "Data Source")

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
data_source = dbutils.widgets.get("data_source")

base_path = f'/Volumes/fmcg/raw/{data_source}/*.csv'

# COMMAND ----------

df = (spark.read
      .format("csv")
      .option("header", "true")
      .option("inferSchema", "true")
      .load(base_path)
      .withColumn("read_timestamp", F.current_timestamp())
      .select("*", "_metadata.file_name", "_metadata.file_size")
)

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("delta.enableChangeDataFeed", "true") \
    .saveAsTable(f"{catalog}.{bronze_schema}.{data_source}")

# COMMAND ----------

# MAGIC %md
# MAGIC ##Silver Processing

# COMMAND ----------

df_bronze = spark.read.table(f"{catalog}.{bronze_schema}.{data_source}")

# COMMAND ----------

df_no_duplicate = df_bronze.dropDuplicates(["customer_id"])
df_trimmed_name = df_no_duplicate.withColumn("customer_name", F.trim(F.col("customer_name")))

# COMMAND ----------

city_mapping = {
    "Bengalore": "Bengaluru",
    "Bengaluruu": "Bengaluru",
    "Hyderabadd": "Hyderabad",
    "Hyderbad": "Hyderabad",
    "NewDelhee": "New Delhi",
    "NewDelhi": "New Delhi",
    "NewDheli": "New Delhi"
}

allowed = ["Bengaluru", "Hyderabad", "New Delhi"]

df_better = (
    df_trimmed_name.replace(city_mapping, subset=["city"])
    .withColumn("city", 
                F.when(F.col("city").isNull(), F.lit(None))
                .when(F.col("city").isin(allowed), F.col("city"))
                .otherwise(F.lit(None))
            )
    .withColumn("customer_name",
                F.when(F.col("customer_name").isNull(), F.lit(None))
                .otherwise(F.initcap(F.col("customer_name")))
            )
    )

# COMMAND ----------

cust_city_fix = {
    789403: "New Delhi",
    789420: "Bengaluru",
    789521: "Hyderabad",
    789603: "Hyderabad"
}

df_city_fix = spark.createDataFrame(
    [(k, v) for k, v in cust_city_fix.items()],
    ["customer_id", "city"]
) 

# COMMAND ----------

df_fixed_city = (
    df_better.alias("df_better").join(df_city_fix.alias("df_city_fix"), 
                           F.col("df_better.customer_id") == F.col("df_city_fix.customer_id"), 
                           how="left")
    .select(F.col("df_better.customer_id").cast("string"),
             F.col("customer_name"),
             F.when(F.col("df_better.city").isNotNull(), F.col("df_better.city"))
             .otherwise(F.col("df_city_fix.city")).alias("city"),
             F.col("read_timestamp"),
             F.col("file_name"),
             F.col("file_size"))
)
df_fixed_city.printSchema()
df_fixed_city.show(truncate=False)

# COMMAND ----------

df_silver = df_fixed_city.select(
    F.col("*"),
    F.when(F.col("city").isNull(), F.concat(F.col("customer_name"), F.lit("-"),F.lit("Unknown")))
    .otherwise(F.concat(F.col("customer_name"), F.lit("-"), F.col("city"))).alias("customer"),
    F.lit("India").alias("market"),
    F.lit("Sports Bar").alias("platform"),
    F.lit("Acquisition").alias("channel")
)

df_silver.printSchema()

# COMMAND ----------

print(data_source)

# COMMAND ----------

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("delta.enableChangeDataFeed", "true") \
    .option("mergeSchema", "true") \
    .saveAsTable(f"{catalog}.{silver_schema}.{data_source}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold Processing

# COMMAND ----------

df_gold = df_silver.select(
    F.col("customer_id"),
    F.col("customer_name"),
    F.col("city"),
    F.col("customer"),
    F.col("market"),
    F.col("platform"),
    F.col("channel")
    )

# COMMAND ----------

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("delta.enableChangeDataFeed", "true") \
    .option("mergeSchema", "true") \
    .saveAsTable(f"{catalog}.{gold_schema}.sb_dim_{data_source}")

# COMMAND ----------

delta_table = DeltaTable.forName(spark, "fmcg.gold.dim_customers")
df_child_table = spark.table("fmcg.gold.sb_dim_customers").select(
    F.col("customer_id").alias("customer_code"),
    F.col("customer"),
    F.col("market"),
    F.col("platform"),
    F.col("channel")
)

# COMMAND ----------

delta_table.alias("target").merge(
    source=df_child_table.alias("source"),
    condition="target.customer_code = source.customer_code"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()