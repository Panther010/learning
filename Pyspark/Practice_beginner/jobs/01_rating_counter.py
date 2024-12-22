from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("movie ratings counter").master("local").getOrCreate()

input_path = "../input_data/u.data"

movie_data = spark.read.csv(input_path, header=False, sep='\t')

col_names = ['user_id', 'movie_id', 'rating', 'date_time']

movie_data = movie_data.toDF(*col_names)
movie_data.createOrReplaceTempView('movie')

rating_count = movie_data  \
                .select(f.col('rating'))  \
                .groupby(f.col('rating'))  \
                .agg(f.count(f.col('rating')).alias('rating_count'))  \
                .orderBy(f.col('rating'))

query = """select rating, count(1) as rating_count from movie group by rating order by rating"""

sql_rating_counter = spark.sql(query)

rating_count.printSchema()

rating_count.show()

sql_rating_counter.show()
