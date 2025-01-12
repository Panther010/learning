import math

from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = SparkSession.builder.appName("distance calculator").master("local").getOrCreate()

input_file = "../output/citibike_ingest"
output_path = "../output/citibike_distance"
citi_bike = spark.read.parquet(input_file)

print(citi_bike.count())
citi_bike.printSchema()
citi_bike.show()
r = 6371e3

def haversine(lat1, long1, lat2, long2):
    lat1_r, long1_r, lat2_r, long2_r = map(math.radians, [lat1, long1, lat2, long2])

    delta_lat = lat1_r - lat2_r
    delta_long = long1_r - long2_r

    a = math.sin(delta_lat/2) ** 2 + (math.cos(lat1_r) * math.cos(lat2_r) * math.sin(delta_long/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r * c/ 1000

haversine_udf = f.udf(haversine, DoubleType())

citi_bike_distance = citi_bike.select(f.col('tripduration'),
                     f.col('start_station_latitude'),
                     f.col('start_station_longitude'),
                     f.col('end_station_latitude'),
                     f.col('end_station_longitude'),
                     f.radians(f.col('start_station_latitude')).alias('lat1'),
                     f.radians(f.col('start_station_longitude').alias('long1')),
                     f.radians(f.col('end_station_latitude')).alias('lat2'),
                     f.radians(f.col('end_station_longitude')).alias('long2'),
                     (f.radians(f.col('start_station_latitude')) - f.radians(f.col('end_station_latitude'))).alias(
                         'lat_delta'),
                     (f.radians(f.col('start_station_longitude')) - f.radians(f.col('end_station_longitude'))).alias(
                         'long_delta')
                     ) \
        .withColumn('a',
                    (f.sin(f.col('lat_delta') / 2) ** 2) +
                    (f.cos(f.col('lat1'))) * (f.cos(f.col('lat2'))) * (f.sin(f.col('long_delta') / 2) ** 2)) \
        .withColumn('c', f.lit(2) * f.atan2(f.sqrt(f.col('a')), f.sqrt(f.lit(1) - f.col('a')))) \
        .withColumn('distance', f.lit(r) * f.col('c') / f.lit(1000))

new_method = citi_bike.withColumn('distance',
                                  haversine_udf(f.col('start_station_latitude'),
                                                f.col('start_station_longitude'),
                                                f.col('end_station_latitude'),
                                                f.col('end_station_longitude')))

citi_bike_distance.printSchema()
citi_bike_distance.show()

new_method.printSchema()
new_method.show()
