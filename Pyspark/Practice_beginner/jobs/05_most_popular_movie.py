from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = SparkSession.builder.appName('most popular movie').master('local').getOrCreate()

movie_rating_file = '../../input_data/u.data'
movie_name_file = '../../input_data/u.item'

name_schema = StructType([StructField('movie_id', IntegerType(), True),
                          StructField('movie_name', StringType(), True)])

ratings = spark.read.csv(movie_rating_file, header=False, inferSchema=True, sep='\t')
names = spark.read.csv(movie_name_file, header=False, sep='|', inferSchema=True, schema=name_schema)
col_names = ['user_id', 'movie_id', 'rating', 'date_time']

ratings = ratings.toDF(*col_names)
names.printSchema()
ratings.createOrReplaceTempView('ratings')
names.createOrReplaceTempView('names')
ratings.printSchema()

ratings.show()
names.show()

popular_movie = ratings.alias('ratings').join(f.broadcast(names.alias('names')),
                                                     f.col('ratings.movie_id') == f.col('names.movie_id')) \
                .groupby(f.col('ratings.movie_id'), f.col('names.movie_name')) \
                 .agg(f.count(f.col('ratings.rating')).alias('rating_counter')) \
                 .select(f.col('names.movie_name'), f.col('ratings.movie_id'), f.col('rating_counter')) \
                 .orderBy(f.col('rating_counter').desc())

query = """select 
                a.movie_name, 
                b.movie_id, 
                count(b.rating) as rating_counter
            from ratings b left join names a 
                on b.movie_id = a.movie_id
            group by b.movie_id, a.movie_name
            order by count(b.rating) desc
            """
popular_movie.show()

popular_sql = spark.sql(query)

popular_sql.printSchema()
popular_sql.show()
