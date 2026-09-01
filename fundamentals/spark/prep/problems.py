from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import *

spark = SparkSession.builder.appName('checking').master('local').getOrCreate()

data = [
    ("AAPL", "2026-06-01", 150.0),
    ("AAPL", "2026-06-02", 155.0),
    ("AAPL", "2026-06-03", 152.0),
    ("AAPL", "2026-06-04", 160.0),
    ("AAPL", "2026-06-05", 158.0),
]

schema = StructType([
    StructField("ticker", StringType()),
    StructField("date", StringType()),
    StructField("price", DoubleType()),
])

df = spark.createDataFrame(data, schema)

# df.show()
# df.printSchema()

window_speac = Window.orderBy(F.col('date')).rowsBetween(-2, 0)
#df.withColumn(
#    'moving_avg',
#    F.round(F.avg(F.col('price')).over(window_speac), 2)
#).show()



data2 = [
    ("Alice", "2026-06-01"),
    ("Alice", "2026-06-02"),
    ("Alice", "2026-06-03"),  # 3 days streak
    ("Alice", "2026-06-06"),
    ("Bob",   "2026-06-01"),
    ("Bob",   "2026-06-03"),  # break in streak
    ("Bob",   "2026-06-04"),
]

schema2 = StructType([
    StructField("user", StringType()),
    StructField("login_date", StringType()),
])

df2 = spark.createDataFrame(data2, schema2)

df2.printSchema()
df2.show()

win_spec2 = Window.partitionBy(F.col('user')).orderBy(F.col('login_date'))

df2.select(
    F.col('*'),
    F.row_number().over(win_spec2).alias('rn'),
    F.date_sub(F.to_date(F.col('login_date'), 'yyyy-MM-dd'), F.row_number().over(win_spec2)).alias('base_date')
).groupby(F.col('user'), F.col('base_date')).agg(F.count('login_date').alias('consecutive_login')).show()