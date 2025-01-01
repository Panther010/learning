from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("min temp").master('local').getOrCreate()

input_file = '../../input_data/1800.csv'

temperature_data = spark.read.csv(input_file, header=False, inferSchema=True)

columns = ['loc_id', 'date_time', 'data_type', 'temp_f', 'col_5', 'flag', 'col_7', 'col_8']

temperature_data = temperature_data.toDF(*columns)

temperature_data.printSchema()

temperature_data.createOrReplaceTempView('temperature')
spark.sql("select * from temperature").show()

min_query = """select loc_id, 
                min(temp_f) as min_temp_f,
                (min(temp_f) -32) * (5/9) as min_temp_c
            from temperature 
            where data_type = 'TMIN'
            group by loc_id"""

min_results = spark.sql(min_query)

max_query = """select loc_id,
                    max(temp_f) as max_temp_f,
                    (max(temp_f) -32) * (5/9) as max_temp_c
            from temperature 
            where data_type = 'TMAX'
            group by loc_id
                """

max_results = spark.sql(max_query)

df_min = temperature_data \
            .filter(f.col('data_type') == f.lit('TMIN')) \
            .groupby(f.col('loc_id')) \
            .agg(f.min(f.col('temp_f')).alias('min_temp_f'),
                 ((f.min(f.col('temp_f')) - 32) * (5/9)).alias('min_temp_c'))

df_min.printSchema()
df_min.show()

df_max = temperature_data \
            .filter(f.col('data_type') == f.lit('TMAX')) \
            .groupby(f.col('loc_id')) \
            .agg(f.max(f.col('temp_f')).alias('max_temp_f'),
                 ((f.max(f.col('temp_f')) - 32) * (5/9)).alias('max_temp_c'))

df_max.printSchema()
df_max.show()
