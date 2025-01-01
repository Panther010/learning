from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = SparkSession.builder.appName("total order by customer").master("local").getOrCreate()

input_file = '../../input_data/customer-orders.csv'

schema = StructType([StructField('cust_id', IntegerType(), True),
                      StructField('order_id', IntegerType(), True),
                      StructField('amount', FloatType(), True)])

orders = spark.read.csv(input_file, header=False, schema=schema)
orders.printSchema()
orders.createOrReplaceTempView('orders')
orders.show()

cust_orders = orders.groupby(f.col('cust_id')).agg(f.sum(f.col('amount')).alias('total_amount')).orderBy(f.col('total_amount').desc())

cust_orders.printSchema()
cust_orders.show()

query = """select cust_id, sum(amount) as total_amount from orders group by cust_id order by sum(amount) desc"""
cust_ord_s = spark.sql(query)
cust_ord_s.show()
