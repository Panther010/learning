from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = SparkSession.builder.appName("avg friends by age").master("local").getOrCreate()

input_path = '../../input_data/fakefriends.csv'

schema = StructType([StructField('id', IntegerType(), True),
                     StructField('name', StringType(), True),
                     StructField('age', IntegerType(), True),
                     StructField('friends_count', IntegerType(), True)])

friends_data = spark.read.csv(input_path, header=False, schema=schema)

friends_data.createOrReplaceTempView('friends')

query = """select age, 
                sum(friends_count) as total_friends, 
                count(age) as user_count, 
                sum(friends_count)/count(age) as avg_friends_number
            from friends 
            group by age 
            order by age"""

result = spark.sql(query)

age_counter = friends_data.groupby(f.col('age')) \
               .agg(f.sum(f.col('friends_count')).alias('total_friends'),
                    f.count(f.col('age')).alias('user_count')) \
               .select(f.col('age'), f.col('total_friends'), f.col('user_count'),
                       (f.col('total_friends')/f.col('user_count')).alias('avg_friends_count'))

age_counter.show()

result.printSchema()
result.show()
