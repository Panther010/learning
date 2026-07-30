from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('read_and_explore_data').master('local').getOrCreate()

olympic_athletes_df = spark.read.csv('/Users/bakulseth/PycharmProjects/learning/data/raw/olympic/2022/olympic_athletes.csv', inferSchema=True, header=True)

olympic_hosts_df = spark.read.csv('/Users/bakulseth/PycharmProjects/learning/data/raw/olympic/2022/olympic_hosts.csv', inferSchema=True, header=True)

olympic_medals_df = spark.read.csv('/Users/bakulseth/PycharmProjects/learning/data/raw/olympic/2022/olympic_medals.csv', inferSchema=True, header=True)

olympic_results_df = spark.read.csv('/Users/bakulseth/PycharmProjects/learning/data/raw/olympic/2022/olympic_results.csv', inferSchema=True, header=True)

print("olympic_athletes_df")
olympic_athletes_df.printSchema()

olympic_athletes_df.show()

print("olympic_hosts_df")
olympic_hosts_df.printSchema()
olympic_hosts_df.show()

print("olympic_medals_df")
olympic_medals_df.printSchema()
olympic_medals_df.show()

print("olympic_results_df")
olympic_results_df.printSchema()
olympic_results_df.show()