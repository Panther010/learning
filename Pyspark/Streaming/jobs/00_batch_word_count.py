from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f

class BatchWordCount:

    def __init__(self):
        self.input_path = '../data/'
        self.out_path = '../output/counter'

        self.spark = SparkSession.builder \
            .appName('batch word count') \
            .master('local') \
            .getOrCreate()

    def read_raw_data(self):
        lines = self.spark.read.text(self.input_path, lineSep='.')
        return lines.select(f.explode(f.split(f.col('value'), ' ')).alias('word'))

    def clean_data(self, raw_df: DataFrame):
        return raw_df.select(f.lower(f.trim(f.col('word'))).alias('word')) \
                .filter((f.col('word').rlike('[a-z]')) & (f.col('word').isNotNull()))

    def word_counter(self, clean_df: DataFrame):
        return clean_df.groupby(f.col('word')).agg(f.count())

    def writer(self, word_count_df: DataFrame):
        word_count_df.write.parquet(self.out_path, mode='overwrite')

    def counter(self):
        print("Starting to run the code")
        raw = self.read_raw_data()
        clean_df = self.clean_data(raw)
        word_cnt = self.word_counter(clean_df)
        self.writer(word_cnt)
        print(f"complete the process total records {word_cnt.count()}")


if __name__ == '__main__':
    word_count = BatchWordCount()
    word_count.counter()