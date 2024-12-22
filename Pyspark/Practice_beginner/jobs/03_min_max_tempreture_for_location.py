from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("min temp").master('local').getOrCreate()

input_file = '../input_data/1800.csv'

temperature_data = spark.read.csv(input_file, header=False, inferSchema=True)

columns = ['loc_id', 'date_time', 'data_type', 'temp_f', 'col_5', 'flag', 'col_7', 'col_8']

temperature_data = temperature_data.toDF(*columns)

temperature_data.printSchema()
temperature_data.show()

temperature_data.createOrReplaceTempView('temperature')
spark.sql("select * from temperature").show()

query = """select loc_id, 
                min(temp_f) as min_temp_f
            from temperature 
            where data_type = 'TMIN'
            group by loc_id"""

results = spark.sql(query)

results.printSchema()
results.show()
