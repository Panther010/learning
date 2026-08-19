# Databricks notebook source
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %run /Workspace/Users/bakulseth001@gmail.com/fmcg_project/utilities

# COMMAND ----------

dbutils.widgets.text("catalog", "fmcg", "Catalog")
dbutils.widgets.text("data_source", "products", "Data Source")

catalog = dbutils.widgets.get("catalog")
data_source = dbutils.widgets.get("data_source")

base_path = f'/Volumes/fmcg/raw/{data_source}/*.csv'
print(base_path)

# COMMAND ----------

df_bronze = (spark.read
          .format("csv")
          .option("header", True)
          .option("inferSchema", True)
          .load(base_path)
          .withColumn("read_timestamp", F.current_timestamp())
          .select("*", "_metadata.file_name", "_metadata.file_size"))

# COMMAND ----------

df_bronze.write \
    .format("delta") \
    .mode("overwrite") \
    .option("deltaEnableChangeDataFeed", "true") \
    .saveAsTable(f"{catalog}.{bronze_schema}.{data_source}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## silver processing

# COMMAND ----------

df_no_dup = df_bronze.dropDuplicates(["product_id"])

# COMMAND ----------

df_better = df_no_dup.select(
    F.regexp_replace(F.col("product_name"), "(?i)protien", "Protein").alias("product_name"),
    F.when(F.col("product_id").rlike(r"^-?\d+(\.\d+)?$"), F.col("product_id"))
        .otherwise(F.lit(99999999)).alias("product_id"),
    F.initcap(F.col("category")).alias("category"),
    F.col("read_timestamp"),
    F.col("_metadata.file_name"),
    F.col("_metadata.file_size"),
    F.regexp_extract(F.col("product_name"), r"\((.*?)\)", 1).alias("variant"),
    F.trim(F.regexp_replace(F.col("product_name"), r"\((.*?)\)", "")).alias("product"),
    F.sha2("product_id", 256).alias("product_code")
)

display(df_better)
display(df_better.select(F.col("category")).distinct())

# COMMAND ----------

df_silver = (df_better
                    .withColumn("division", 
                                F.when(F.col("category") == "Healthy Snacks", "Healthy Snacks")
                                .when(F.col("category") == "Energy Bars", "Nutrition Bar")
                                .when(F.col("category") == "Granola & Cereals", "Breakfast Foods")
                                .when(F.col("category") == "Recovery Dairy", "Dairy & Recovery")
                                .when(F.col("category") == "Protien Bars", "Nutrition Bar")
                                .when(F.col("category") == "Electrolyte Mix", "Hydration & Electrolytes")
                                .otherwise(F.lit("Unknown")))
                   )

display(df_silver)

# COMMAND ----------

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("delta.enableChangeDataFeed", "true") \
    .option("mergeSchema", "true") \
    .saveAsTable(f"{catalog}.{silver_schema}.{data_source}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## gold processing

# COMMAND ----------

df_gold = df_silver.select(
    "product_code",
    "division",
    "category",
    "product",
    "variant"
)
display(df_gold)

# COMMAND ----------

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("delta.enableChangeDataFeed", "true") \
    .option("mergeSchema", "true") \
    .saveAsTable(f"{catalog}.{gold_schema}.sb_dim_{data_source}")

# COMMAND ----------

delta_table = DeltaTable.forName(spark, "fmcg.gold.dim_products")
delta_table.alias("target").merge(
    source=df_gold.alias("source"),
    condition="target.product_code = source.product_code"
).whenMatchedUpdate(
    set={
        "division": "source.division",
        "category": "source.category",
        "product": "source.product",
        "variant": "source.variant"
    }
).whenNotMatchedInsert(
    values={
        "product_code": "source.product_code",
        "division": "source.division",
        "category": "source.category",
        "product": "source.product",
        "variant": "source.variant"
    }
).execute()