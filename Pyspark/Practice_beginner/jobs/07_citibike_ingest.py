from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("citi bike ingest").master('local').getOrCreate()

input_file = '../input_data/citibike.csv'
output_path = '../output/citibike_ingest'

citibike_raw = spark.read.csv(input_file, header=True, inferSchema=True)

citibike_raw.printSchema()

updated_columns = [col.replace(" ", "_") for col in citibike_raw.columns]

citibike_clean = citibike_raw.toDF(*updated_columns)

citibike_clean.printSchema()
print(citibike_clean.count())
citibike_clean.write.parquet(output_path, mode='overwrite')
