# Databricks notebook source
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %run /Workspace/Users/bakulseth001@gmail.com/fmcg_project/utilities

# COMMAND ----------

dbutils.widgets.text("catalog", "fmcg", "Catalog")
dbutils.widgets.text("data_source", "orders", "Data Source")

catalog = dbutils.widgets.get("catalog")
data_source = dbutils.widgets.get("data_source")

base_path = f"/Volumes/fmcg/raw/{data_source}"
landing_path = f"{base_path}/landing"
processed_path = f"{base_path}/processed"

print(f"base_path: {base_path}")
print(f"landing_path: {landing_path}")
print(f"processed_path: {processed_path}")

# COMMAND ----------

bronze_df = (spark.read
             .format("csv")
             .option("inferSchema", "true")
             .option("header", "true")
             .load(landing_path)
             .withColumn("read_timestamp", F.current_timestamp())
             .select(
                 "*",
                 "_metadata.file_name",
                 "_metadata.file_size"
             )

)

# COMMAND ----------

bronze_df.write \
    .format("delta") \
    .mode("append") \
    .option("deltaEnabledChnagedataFeed", "true") \
    .saveAsTable(f"{catalog}.{bronze_schema}.{data_source}")

# COMMAND ----------

files = dbutils.fs.ls(landing_path)
for file_info in files:
    dbutils.fs.mv(
        file_info.path,
        processed_path
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver processing

# COMMAND ----------

df_bronze = spark.read.table(f"{catalog}.{bronze_schema}.{data_source}")

# COMMAND ----------

df_fixed = (df_bronze
            .filter(F.col("order_qty").isNotNull())
            .withColumn(
                "customer_id",
                F.when(F.col("customer_id").rlike("[^0-9]"), "999999")
                .otherwise(F.col("customer_id"))
            )
        )

df_date_fix = df_fixed.withColumn(
    "order_placement_date",
    F.regexp_replace(F.col("order_placement_date"), "^[A-Za-z]+,\\s*", "")
).withColumn(
    "order_placement_date",
    F.coalesce(
        F.try_to_date(F.col("order_placement_date"), "dd/MM/yyyy"),
        F.try_to_date(F.col("order_placement_date"), "yyyy/MM/dd"),
        F.try_to_date(F.col("order_placement_date"), "dd-MM-yyyy"),
        F.try_to_date(F.col("order_placement_date"), "MMMM dd, yyyy"),
    )
)

df_removed_dup = df_date_fix.dropDuplicates(["order_id", "order_placement_date", "customer_id", "product_id", "order_qty"])

df_fix_product_id = df_removed_dup.withColumn("product_id", F.col("product_id").cast("string"))

# COMMAND ----------

df_date_fix.printSchema()
df_date_fix.count()
df_removed_dup.count()

# COMMAND ----------

df_date_fix.select("order_id", "order_placement_date", "customer_id", "product_id", "order_qty").distinct().count()

# COMMAND ----------

df_product = spark.table(f"{catalog}.{silver_schema}.products")

df_joined = df_date_fix.alias("order").join(
    df_product.alias("product"), 
    F.col("order.product_id") == F.col("product.product_id"), 
    how="left").select(
        "order.*",
        "product.product_code")

df_joined.show(truncate=False)

# COMMAND ----------

if not (spark.catalog.tableExists(f"{catalog}.{silver_schema}.{data_source}")):
    df_joined.write \
        .format("delta") \
        .mode("overwrite") \
        .option("delta.enableChangeDataFeed", "true") \
        .option("mergeSchema", "true") \
        .saveAsTable(f"{catalog}.{silver_schema}.{data_source}")
else:
    silver_delta = DeltaTable.forName(spark, f"{catalog}.{silver_schema}.{data_source}")
    silver_delta.alias("silver").merge(
        df_joined.alias("updates"),
        "silver.order_id = updates.order_id AND silver.order_placement_date = updates.order_placement_date AND silver.customer_id = updates.customer_id AND silver.product_id = updates.product_id") \
    .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gold processing

# COMMAND ----------

df_gold = spark.sql(f"select order_id, order_placement_date as date, customer_id as customer_code, product_code, product_id, order_qty as sold_quantity from {catalog}.{silver_schema}.{data_source}")
df_gold = df_gold.withColumn(
    "product_code",
    F.coalesce(F.col("product_code"), F.sha2(F.col("product_id").cast("string"), 256))
)
display(df_gold.limit(20))

# COMMAND ----------

if not (spark.catalog.tableExists(f"{catalog}.{gold_schema}.sb_fact_{data_source}")):
    df_gold.write \
        .format("delta") \
        .mode("overwrite") \
        .option("delta.enableChangeDataFeed", "true") \
        .option("mergeSchema", "true") \
        .saveAsTable(f"{catalog}.{gold_schema}.sb_fact_{data_source}")
else:
    gold_delta = DeltaTable.forName(spark, f"{catalog}.{gold_schema}.sb_fact_{data_source}")
    gold_delta.alias("gold").merge(
        df_gold.alias("updates"),
        "gold.order_id = updates.order_id AND gold.date = updates.date AND gold.customer_code = updates.customer_code AND gold.product_code = updates.product_code") \
    .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

# COMMAND ----------

# MAGIC %md
# MAGIC Merge data with parent company

# COMMAND ----------

df_child = spark.sql(f"select date, product_code, customer_code, sold_quantity from {catalog}.{gold_schema}.sb_fact_{data_source}")
df_child.show(500, truncate=False)

# COMMAND ----------

df_monthly = (df_child
              .withColumn("month_start", F.trunc(F.col("date"), "MM"))
              .groupBy(F.col("month_start"), F.col("product_code"), F.col("customer_code"))
              .agg(F.sum("sold_quantity").alias("sold_quantity"))
              .withColumnRenamed("month_start", "date"))

df_monthly.show(truncate=False)

# COMMAND ----------

parent_delta = DeltaTable.forName(spark, f"{catalog}.{gold_schema}.fact_{data_source}")
parent_delta.alias("parent").merge(
    df_monthly.alias("update"),
    "parent.date = update.date AND parent.product_code = update.product_code AND parent.customer_code = update.customer_code") \
.whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()