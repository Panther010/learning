# Databricks notebook source
from pyspark.sql import functions as F
from delta.tables import DeltaTable

from pyspark.sql.window import Window

# COMMAND ----------

# MAGIC %run /Workspace/Users/bakulseth001@gmail.com/fmcg_project/utilities

# COMMAND ----------

dbutils.widgets.text("catalog", "fmcg", "Catalog")
dbutils.widgets.text("data_source", "gross_price", "Data Source")

catalog = dbutils.widgets.get("catalog")
data_source = dbutils.widgets.get("data_source")

base_path = f'/Volumes/fmcg/raw/{data_source}/*.csv'
print(base_path)

# COMMAND ----------

bronze_df = (spark.read
             .format("csv")
             .option("inferSchema", "true")
             .option("header", "true")
             .load(base_path)
             .withColumn("read_timestamp", F.current_timestamp())
             .select("*", "_metadata.file_name", "_metadata.file_size")
)

# COMMAND ----------

bronze_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("deltaEnabledChangeDataFeed", "true") \
    .saveAsTable(f"{catalog}.{bronze_schema}.{data_source}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver processing

# COMMAND ----------

display(bronze_df.select("gross_price").distinct())

# COMMAND ----------

df_month_fix = bronze_df.withColumn(
    "month",
    F.coalesce(
        F.try_to_date(F.col("month"), "yyyy/MM/dd"),
        F.try_to_date(F.col("month"), "dd/MM/yyyy"),
        F.try_to_date(F.col("month"), "yyyy-MM-dd"),
        F.try_to_date(F.col("month"), "dd-MM-yyyy"),

        )
)

# COMMAND ----------

df_gross_price_fix = df_month_fix.withColumn(
    "gross_price",
    F.when(F.col("gross_price").rlike(r"^-?\d+(\.\d+)?$"), 
           F.when(F.col("gross_price") < 0, (-1 * F.col("gross_price")).cast("double"))
           .otherwise(F.col("gross_price").cast("double")))
    .otherwise(F.lit(0).cast("double"))
    )

display(df_gross_price_fix)
df_gross_price_fix.printSchema()

# COMMAND ----------

# DBTITLE 1,sts
# MAGIC %sql
# MAGIC select * from fmcg.silver.products

# COMMAND ----------

df_product = spark.table(f"{catalog}.{silver_schema}.products")
df_silver = df_gross_price_fix.alias("price").join(
    df_product.alias("product"),
    F.col("price.product_id") == F.col("product.product_id"),
    "left"
    ).select(
        F.col("price.*"),
        F.coalesce(F.col("product.product_code"), 
                   F.sha2(F.col("price.product_id").cast("string"), 256)).alias("product_code"))
    
display(df_silver.filter(F.col("product_id") == F.lit(88888888)))

# COMMAND ----------

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("delta.enableChangeDataFeed", "true") \
    .option("mergeSchema", "true") \
    .saveAsTable(f"{catalog}.{silver_schema}.{data_source}")

# COMMAND ----------

df_gold = df_silver.select(
    "product_code", "gross_price", "month"
)

# COMMAND ----------

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("delta.enableChangeDataFeed", "true") \
    .saveAsTable(f"{catalog}.{gold_schema}.sb_dim_{data_source}")

# COMMAND ----------

display(df_gold)

# COMMAND ----------

window_spec = Window.partitionBy(F.col("product_code")).orderBy(F.col("is_zero"), F.col("year").desc(), F.col("date_month").desc())
df_gold_year = (df_gold
                .withColumn("is_zero", 
                            F.when(F.col("gross_price") == 0, F.lit(1))
                            .otherwise(F.lit(0)))
                .withColumn("year", F.year(F.col("month")))
                .withColumn("date_month", F.date_format(F.col("month"), "MM"))
                .withColumn("rnk", F.row_number().over(window_spec)))

display(df_gold_year)

# COMMAND ----------

df_final = df_gold_year.filter(
    F.col("rnk") == 1).select(
    F.col("product_code"), 
    F.col("gross_price").alias("price_inr"), 
    F.col("year"))

display(df_final)

# COMMAND ----------

delta_table = DeltaTable.forName(spark, "fmcg.gold.dim_gross_price")

delta_table.alias("target").merge(
    source=df_final.alias("source"),
    condition="target.product_code = source.product_code"
).whenMatchedUpdate(
    set={
        "price_inr": F.col("source.price_inr"),
        "year": F.col("source.year")
    }
).whenNotMatchedInsert(
    values={
        "product_code": F.col("source.product_code"),
        "price_inr": F.col("source.price_inr"),
        "year": F.col("source.year")
    }
).execute()
