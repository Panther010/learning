from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging
from pyspark.sql.window import Window


class IngestFlightData:

    def __init__(self):

        self.spark = SparkSession.builder.appName('Flight_analysis').master('local').getOrCreate()

        # Define Input and Output Paths
        self.flight_data = '../../../input_data/raw/flightData.csv'
        self.passengers = '../../../input_data/raw/passengers.csv'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def read_flight_data(self) -> DataFrame:
        self.log.info(f'reading data from {self.flight_data}')
        return self.spark.read.csv(self.flight_data, inferSchema=True, header=True)


    def read_passenger_data(self):
        self.log.info(f'reading data from {self.passengers}')
        return self.spark.read.csv(self.passengers, inferSchema=True, header=True)

    def flight_per_month(self, fights_df: DataFrame) -> DataFrame:
        self.log.info(f'starting flights analysis Q1')
        flights_d = fights_df.select(
            f.col('flightId'),
            f.month(f.col('date')).alias('flight_month')).dropDuplicates()

        flights_per_month = flights_d.groupby(f.col('flight_month')) \
                             .agg(f.count(f.col('flightId')).alias('flight_count')).orderBy(f.col('flight_month'))
        return flights_per_month

    def frequent_flyer(self, flight: DataFrame, passengers: DataFrame) -> DataFrame:
        self.log.info(f'starting flights analysis Q2')
        # check if drop duplicate is required or not
        result = flight.alias('flight') \
            .select(f.col('passengerId'), f.col('flightId')) \
            .dropDuplicates() \
            .groupby(f.col('passengerId')).agg(f.count(f.col('flightId')).alias('flight_count')) \
            .join(passengers.alias('passengers'),
                  f.col('flight.passengerId') == f.col('passengers.passengerId')) \
            .orderBy(f.col('flight_count').desc())
        return result

    def country_visitor(self, flight: DataFrame) -> DataFrame:
        self.log.info(f'starting flights analysis Q3')
        countries = flight.select(
            f.col('passengerId'),
            f.col('from').alias('country'),
            f.col('date').alias('travel_date'))

        last_country = flight.withColumn('',
                                         f.rank().over(Window.partitionBy(f.col('passengerId'))
                                                       .orderBy(f.col('date').desc())).alias('rn')) \
            .filter(f.col('rn') == f.lit(1)) \
            .select(f.col('passengerId'),
                    f.col('to').alias('country'), f.dateadd(f.col('date'), 1).alias('travel_date'))

        all_countries = countries.union(last_country) \
            .withColumn('is_uk', f.when(f.col('country') == f.lit('uk'), f.lit(1)).otherwise(f.lit(0))) \
            .withColumn('seq',
                        f.sum('is_uk').over(Window.partitionBy(f.col('passengerId')).orderBy(f.col('travel_date')))) \
            .filter(f.col('country') != f.lit('uk')) \
            .select(f.col('passengerId'), f.col('seq'), f.col('country')).dropDuplicates() \
            .groupby(f.col('passengerId'), f.col('seq')).agg(f.count(f.col('country')).alias('country_count')) \
            .groupby(f.col('passengerId')).agg(f.max('country_count').alias('longest_run'))

        return all_countries

    def fly_together(self, flight: DataFrame) -> DataFrame:
        self.log.info(f'starting flights analysis Q4')
        result1 = flight.alias('fl1').join(
            flight.alias('fl2'),
            (f.col('fl1.flightId') == f.col('fl2.flightId')) &
            (f.col('fl1.passengerId') < f.col('fl2.passengerId')) ) \
            .select(f.col('fl1.*'), f.col('fl2.passengerId').alias('co_passenger_id'))

        result1.show(1000)

        result = result1.groupby(f.col('passengerId'), f.col('co_passenger_id')) \
            .agg(f.count(f.col('fl1.flightId')).alias('flight_together')) \
            .filter(f.col("flight_together") > f.lit(3))

        result.show(1000)
        print(result.count())

        return result

    def main(self) -> None:
        self.log.info(f'Starting to analyse flight data')
        flight_data_df = self.read_flight_data()
        passengers_df = self.read_passenger_data()

        monthly_flight_df = self.flight_per_month(flight_data_df)
        monthly_flight_df.printSchema()
        # monthly_flight_df.show()

        frequent_flyer_df = self.frequent_flyer(flight_data_df, passengers_df)
        frequent_flyer_df.printSchema()
        # frequent_flyer_df.show()

        country_visit_df = self.country_visitor(flight_data_df)
        country_visit_df.printSchema()
        # country_visit_df.show(100)

        flight_together_df = self.fly_together(flight_data_df)
        flight_together_df.printSchema()

if __name__ == '__main__':
    flights = IngestFlightData()
    flights.main()