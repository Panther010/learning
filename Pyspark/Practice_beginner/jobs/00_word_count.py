"""
This PySpark program performs a word count analysis on a text file, filtering out common stop words,
and outputs the results sorted by frequency using both DataFrame API and SQL.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as f


class WordsCount:

    def __init__(self):
        # 1. Initialize Spark Session
        self.spark = SparkSession.builder.appName('wc').master('local').getOrCreate()

        # file paths
        self.input_path = "../input_data/words.txt"
        self.output_path = "../output/words_count"

        # 2. Define File Paths for Input and Output
        self.stop_words = ["is", "the", "a", "an", "and", "to", "in", "of", "on", "for", "with", "at", " ", "he", "she",
                      "his", "was", "had", "that", "it", "as", ""]
        self.stop_words_str = ",".join([f"'{word}'" for word in self.stop_words])
        print(self.stop_words_str)

    # Read Data from Input File
    def read_data(self):
        return self.spark.read.text(self.input_path)

    # Split Words and Filter Stop Words using DataFrame API
    def split_words(self, line_df):
        return line_df.select(
            f.explode(
                f.split(
                    f.lower(f.col('value'))
                , ' ')).alias('words')
            )

    # Clean the words by removing Null, unwanted characters and filter unwanted words
    def words_cleaner(self, words_df):
        return words_df.withColumn('words', f.regexp_replace(f.col('words'), r'[^a-z]', '')) \
            .filter(~f.col('words').isin(self.stop_words) & f.col('words').isNotNull())

    # Count Words and Order by Frequency
    def words_counter(self, words_df):
        return words_df.groupby('words').agg(f.count('words').alias('words_count'))

    # write the data to output directory
    def writer(self, word_count_df):
        word_count_df.printSchema()
        word_count_df.orderBy(f.col('words_count').desc()).show()
        print(word_count_df.count())
        # word_count_df.write.parquet(self.output_path)

    def sql_wc(self, lines_df):
        lines_df.createOrReplaceTempView("lines")
        return self.spark.sql(f"""
        with words_tb as (
                select explode(split(lower(value), " ")) as words from lines),
            clean_words_tb as (
                select regexp_replace(words, '[^a-z]', '') as words from words_tb)
            select 
                words, 
                count(1) as words_count 
            from clean_words_tb
            where words not in ({self.stop_words_str}) 
            group by words 
            order by count(1) desc
        """)

    # diver program
    def execute(self):
        lines = self.read_data()
        words = self.split_words(lines)
        clean_words = self.words_cleaner(words)
        words_count = self.words_counter(clean_words)
        self.writer(words_count)

        sql_wc_data = self.sql_wc(lines)
        sql_wc_data.show()
        self.spark.stop()


if __name__ == '__main__':
    wc = WordsCount()
    wc.execute()