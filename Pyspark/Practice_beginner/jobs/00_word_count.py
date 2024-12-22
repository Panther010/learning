from pyspark.sql import SparkSession
from pyspark.sql import functions as f

# 1. Initialize Spark Session
spark = SparkSession.builder.appName("00 word count").master("local").getOrCreate()

# file paths
input_path = "../input_data/words.txt"
output_path = "../output/words_count"

# 2. Define File Paths for Input and Output
stop_words = ["is", "the", "a", "an", "and", "to", "in", "of", "on", "for", "with", "at", " ", "he", "she", "his", "was", "had", "that", "it", "as", ""]
stop_words_str = ",".join([f"'{word}'" for word in stop_words])
print(stop_words_str)

# 4. Read Data from Input File
df = spark.read.text(input_path)
df.createOrReplaceTempView("book_data")

# 5. Split Words and Filter Stop Words using DataFrame API
df_words = df.select(
    f.explode(  # convert all the words into separate row
        f.split(  # split the words on spaces
            f.lower(f.col("value")),
            " ")).alias("words")) \
    .filter(~f.col("words").isin(stop_words))

# 6. Count Words and Order by Frequency
df_words_count = df_words.groupby(f.col("words"))  \
                  .agg(f.count("words").alias("words_count"))  \
                  .orderBy(f.col("words_count").desc())

# 7. Alternatively, Using SQL for Word Count
query = f""" with words_tb as (
                select explode(split(lower(value), " ")) as words from book_data)
            select 
                words, 
                count(1) as words_count 
            from words_tb
            where words not in ({stop_words_str}) 
            group by words 
            order by count(1) desc"""

result = spark.sql(query)

result.coalesce(1).write.csv(output_path, mode="overwrite", header=True)

spark.stop()
