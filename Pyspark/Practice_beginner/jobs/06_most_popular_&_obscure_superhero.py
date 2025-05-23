from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = SparkSession.builder.appName('popular hero').master('local').getOrCreate()

hero_graphs = '../input_data/Marvel-graph.txt'
hero_names = '../input_data/Marvel-names.txt'

graphs = spark.read.text(hero_graphs)

name_schema = StructType([StructField('hero_id', IntegerType(), True),
                          StructField('hero_name', StringType(), True)])

names = spark.read.csv(hero_names, sep=' ', header=False, inferSchema=True, schema=name_schema)

graphs.printSchema()
graphs.show()

heroes = graphs.select(f.split(f.col('value'), ' ')[0].alias('hero_id'),
                       (f.size(f.split(f.col('value'), ' ')) - 1).alias('connection')) \
          .groupby(f.col('hero_id')).agg(f.sum(f.col('connection')).alias('total_connections'))


heroes.printSchema()
heroes.show()

names.printSchema()
names.show()

result = heroes.alias('heroes').join(names.alias('names'), f.col('heroes.hero_id') == f.col('names.hero_id')) \
        .select(f.col('heroes.hero_id'), f.col('names.hero_name'), f.col('total_connections')) \
        .orderBy(f.col('total_connections').desc())

result.printSchema()
result.show()

graphs.createOrReplaceTempView('graphs')
names.createOrReplaceTempView('names')

query = """with heroes_and_connections as (
            select 
                split(value, ' ')[0] as hero_id, 
                (size(split(value, ' ')) - 1) as connections 
            from graphs
            )
            select a.hero_id,
                b.hero_name,
                sum(a.connections) as total_connection 
            from heroes_and_connections a inner join names b on a.hero_id = b.hero_id
            group by a.hero_id, b.hero_name
            order by sum(a.connections)
            """

sql_results = spark.sql(query)
sql_results.printSchema()
sql_results.show()
