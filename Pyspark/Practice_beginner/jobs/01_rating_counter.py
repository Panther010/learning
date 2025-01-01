from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from pyspark.sql.types import *


class RatingCounter:

    def __init__(self):
        self.spark = SparkSession.builder.appName("movie ratings counter").master("local").getOrCreate()
        self.input_path = "../../input_data/u.data"
        self.output_path = '../output/ratings_count/'

        self.col_names = ['user_id', 'movie_id', 'rating', 'date_time']

    def get_schema(self):
        return StructType([
            StructField("user_id", IntegerType(), True),
            StructField("movie_id", IntegerType(), True),
            StructField("rating", IntegerType(), True),
            StructField("date_time", StringType(), True)])

    def data_read(self):
        return self.spark.read.csv(self.input_path, schema=self.get_schema(), sep='\t')

    def data_read1(self):
        data = self.spark.read.csv(self.input_path, inferSchema=True, sep='\t')
        data = data.toDF(*self.col_names)
        return data

    def ratings_counter(self, data_df:DataFrame):
        return data_df.groupby('rating').agg(f.count('user_id').alias('ratings_count')).orderBy('ratings_count')

    def ratings_counter_sql(self, movie_data_df):
        movie_data_df.createOrReplaceTempView('movie')
        query = """select rating, count(1) as rating_count from movie group by rating order by rating"""
        return self.spark.sql(query)

    def data_writer(self, ratings_df):
        ratings_df.write.parquet(self.output_path)

    def execute(self):
        movie_data = self.data_read()

        ratings = self.ratings_counter(movie_data)
        ratings.show()

        sql_ratings = self.ratings_counter_sql(movie_data)
        sql_ratings.show()


if __name__ == '__main__':
    rc = RatingCounter()
    rc.execute()
