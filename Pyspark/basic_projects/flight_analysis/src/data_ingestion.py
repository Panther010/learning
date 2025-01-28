from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from pyspark.sql.window import Window
import logging
import time


class IngestFlightData:

    def __init__(self, flight_data: str, passenger_data: str):
        self.spark = SparkSession.builder.appName('Flight_analysis').master('local').getOrCreate()

        # Define Input and Output Paths
        self.flight_data = flight_data
        self.passengers_data = passenger_data

        # Logging setup
        formatter = '%(asctime)s : %(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('FlightAnalysis')

    def read_data(self, file_path: str) -> DataFrame:
        """Read a CSV file and return a Spark DataFrame."""
        self.log.info(f'reading data from {file_path}')
        return self.spark.read.csv(file_path, inferSchema=True, header=True)

    def calculate_monthly_flights(self, flights_df: DataFrame) -> DataFrame:
        """Find the total number of flights for each month."""
        self.log.info(f'Calculating flights per month')
        return flights_df \
            .select(
                f.col('flightId'),
                f.month(f.col('date')).alias('flight_month')) \
            .dropDuplicates() \
            .groupby(f.col('flight_month')) \
            .agg(f.count(f.col('flightId')).alias('flight_count'))

    def find_frequent_flyers(self, flight: DataFrame, passengers: DataFrame) -> DataFrame:
        """Find the names of the 100 most frequent flyers."""
        self.log.info(f'Finding the most frequent flyers')
        # check if drop duplicate is required or not
        return flight.alias('flight') \
            .select(f.col('passengerId'), f.col('flightId')) \
            .groupby(f.col('passengerId')).agg(f.count(f.col('flightId')).alias('flight_count')) \
            .join(f.broadcast(passengers).alias('passengers'), f.col('flight.passengerId') == f.col('passengers.passengerId')) \
            .orderBy(f.col('flight_count').desc(), f.col('flight.passengerId')) \
            .drop(f.col('passengers.passengerId')).limit(100)

    def longest_non_uk_sequence(self, flight: DataFrame) -> DataFrame:
        """Find the longest sequence of countries a passenger visited without being in the UK."""
        self.log.info("Finding longest non-UK country sequences")

        # all the countries where passenger been to
        countries = flight.select(
            f.col('passengerId'),
            f.col('from').alias('country'),
            f.col('date').alias('travel_date'))

        # Last country where passenger is present
        last_country = flight.withColumn('rn',
                                         f.rank().over(Window.partitionBy(f.col('passengerId'))
                                                       .orderBy(f.col('date').desc()))) \
            .filter(f.col('rn') == f.lit(1)) \
            .select(f.col('passengerId'),
                    f.col('to').alias('country'), f.dateadd(f.col('date'), 1).alias('travel_date'))

        # Fetch the longest run without visiting UK
        return countries.union(last_country) \
            .withColumn('is_uk', f.when(f.col('country') == f.lit('uk'), f.lit(1)).otherwise(f.lit(0))) \
            .withColumn('seq',
                        f.sum('is_uk').over(Window.partitionBy(f.col('passengerId')).orderBy(f.col('travel_date')))) \
            .filter(f.col('country') != f.lit('uk')) \
            .select(f.col('passengerId'), f.col('seq'), f.col('country')).dropDuplicates() \
            .groupby(f.col('passengerId'), f.col('seq')).agg(f.count(f.col('country')).alias('country_count')) \
            .groupby(f.col('passengerId')).agg(f.max('country_count').alias('longest_run')) \
            .orderBy(f.col('longest_run').desc())

    def passengers_flying_together(self, flight: DataFrame) -> DataFrame:
        """Find pairs of passengers who have flown together"""
        self.log.info(f'Trying to calculate passengers flown together')
        return flight.alias('fl1').join(
            flight.alias('fl2'),
            (f.col('fl1.flightId') == f.col('fl2.flightId')) &
            (f.col('fl1.passengerId') < f.col('fl2.passengerId'))) \
            .select(f.col('fl1.passengerId'),
                    f.col('fl2.passengerId').alias('co_passenger_id'),
                    f.col('fl1.flightId'),
                    f.col('fl1.date').alias('flight_date'))

    def more_than_three(self, together_df: DataFrame) -> DataFrame:
        """Find pairs of passengers who have been on more than 3 flights together."""
        self.log.info("Finding passengers who have flown together on more than 3 flights")
        return together_df \
            .groupby(f.col('passengerId'), f.col('co_passenger_id')) \
            .agg(f.count(f.col('fl1.flightId')).alias('flight_together')) \
            .filter(f.col("flight_together") > f.lit(3)) \
            .orderBy(f.col('flight_together').desc())

    def flights_together_in_date_range(self,
                                       min_flights: int,
                                       from_date: str,
                                       to_date: str,
                                       together_df: DataFrame) -> DataFrame:
        """Find passengers who have flown together more than `min_flights` times in a given date range."""
        self.log.info(f"Finding passengers who flew together,"
                      f"more than {min_flights} times between {from_date} and {to_date}")
        return together_df.filter(f.col('flight_date').between(f.lit(from_date), f.lit(to_date))) \
            .groupby(f.col('passengerId'), f.col('co_passenger_id')) \
            .agg(f.count(f.col('fl1.flightId')).alias('flight_together'),
                 f.min(f.col('flight_date')).alias('from'),
                 f.max(f.col('flight_date')).alias('to')) \
            .filter(f.col("flight_together") > f.lit(min_flights)) \
            .orderBy(f.col('flight_together').desc())

    def main(self) -> None:
        self.log.info(f'Starting flight analysis .\n')

        # Read data
        start_time = time.time()
        flights_df = self.read_data(self.flight_data).cache()
        passengers_df = self.read_data(self.passengers_data)

        # Q1: Total flights per month
        monthly_flight_df = self.calculate_monthly_flights(flights_df)
        monthly_flight_df.printSchema()
        monthly_flight_df.show()

        # Q2: Frequent flyers
        frequent_flyers_df = self.find_frequent_flyers(flights_df, passengers_df)
        frequent_flyers_df.printSchema()
        frequent_flyers_df.show()

        # Q3: Longest non-UK sequence
        country_visit_non_uk_df = self.longest_non_uk_sequence(flights_df)
        country_visit_non_uk_df.printSchema()
        country_visit_non_uk_df.show(100)

        # Q4: Passengers flying together on more than 3 flights
        flight_together_df = self.passengers_flying_together(flights_df).cache()
        more_than_3_df = self.more_than_three(flight_together_df)
        more_than_3_df.show(100)

        # Q5: Passengers flying together more than `min_flights` times in a given date range.
        more_than_n_df = self.flights_together_in_date_range(7, '2017-01-01', '2017-08-08', flight_together_df)
        more_than_n_df.show(100)
        end_time = time.time()
        print(f"Job started as {start_time} job completed at {end_time} total run time {end_time- start_time}")


if __name__ == '__main__':
    # Replace these with your actual file paths
    flight_data_path = "../../../input_data/raw/flightData.csv"
    passenger_data_path = "../../../input_data/raw/passengers.csv"

    analysis = IngestFlightData(flight_data_path, passenger_data_path)
    analysis.main()