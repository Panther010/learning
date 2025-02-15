from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from src.logger import setup_logger
from src.spark_manager import get_spark_session, stop_spark_session


class FlightAnalysis:

    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark
        self.log = setup_logger()

        self.input_path = '../../../input_data/silver/'
        self.output_path = '../../../input_data/gold/'

    def _read_parquet(self, path: str) -> DataFrame:
        self.log.info(f'reading data from {path}')
        return self.spark.read.parquet(path)

    def _calculate_flights_per_month(self, df: DataFrame) -> DataFrame:
        self.log.info('calculating flights per month')
        per_month = df \
            .groupBy(f.month(f.col('date')).alias('month')) \
            .agg(f.count(f.col('flight_id')).alias('number_of_flight')) \
            .orderBy(f.col('month'))
        per_month.printSchema()
        return per_month

    def _calculate_frequent_flyers(self, flights: DataFrame, passengers: DataFrame) -> DataFrame:
        self.log.info('calculating names of the 100 most frequent flyers.')
        frequent_flyers = flights.alias('flights') \
             .groupBy(f.col('passenger_id')) \
            .agg(f.count(f.col('flight_id')).alias('number_of_flights')) \
            .join(passengers.alias('passengers'),
                  f.col('flights.passenger_id') == f.col('passengers.passenger_id')) \
            .select(f.col('flights.passenger_id'),
                    f.col('number_of_flights'),
                    f.col('first_name'),
                    f.col('last_name')) \
            .orderBy(f.col('number_of_flights').desc()).limit(100)
        frequent_flyers.printSchema()
        return frequent_flyers

    def _calculate_co_passengers(self, df: DataFrame) -> DataFrame:
        self.log.info('passengers who have been on more than 3 flights together')
        co_passengers = df.alias('fl1').join(df.alias('fl2'),
                                             (f.col('fl1.flight_id') == f.col('fl2.flight_id')) &
                                             (f.col('fl1.passenger_id') < f.col('fl2.passenger_id'))) \
            .groupBy(f.col('fl1.passenger_id').alias('passenger_id1'),
                     f.col('fl2.passenger_id').alias('passenger_id2')) \
            .agg(f.count('fl1.flight_id').alias('number_of_flight_together')) \
            .orderBy(f.col('number_of_flight_together').desc()) \
            .filter(f.col('number_of_flight_together') > f.lit(3))
        co_passengers.printSchema()
        return co_passengers

    def _calculate_co_passengers_more_than_n(self, df:DataFrame, at_least_n: int, from_date: str, to_date: str) -> DataFrame:
        self.log.info('passengers who have been on more than N flights together within the range')
        df = df.filter(f.col('date').between(f.lit(from_date), f.lit(to_date)))
        result = df.alias('fl1').join(df.alias('fl2'),
                                      (f.col('fl1.flight_id') == f.col('fl2.flight_id')) &
                                      (f.col('fl1.passenger_id') < f.col('fl2.passenger_id'))) \
            .groupby(f.col('fl1.passenger_id').alias('passenger_id1'),
                     f.col('fl2.passenger_id').alias('passenger_id2')) \
            .agg(f.count('fl1.flight_id').alias('number_of_flight_together'),
                 f.min(f.col('fl1.date')).alias('from_date'),
                 f.max(f.col('fl1.date')).alias('to_date')) \
            .filter(f.col('number_of_flight_together') >= f.lit(at_least_n)) \
            .orderBy(f.col('number_of_flight_together').desc())
        result.printSchema()
        return result

    def _write_csv_to_gold(self, df:DataFrame, path:str) -> None:
        self.log.info(f'Writing data to {path}')
        df.coalesce(1).write \
            .option("header", "true") \
            .option("delimiter", ",") \
            .mode("overwrite").csv(path)

    def main(self) -> None:
        try:
            # read data from silver layer
            flights_details_df = self._read_parquet(f'{self.input_path}flight_details').cache()
            flight_customer_df = self._read_parquet(f'{self.input_path}flights_data').cache()
            passenger_details_df = self._read_parquet(f'{self.input_path}passenger_details').cache()
            passenger_flight_df = self._read_parquet(f'{self.input_path}passenger_flight').cache()

            # Data analysis
            # Q1 Find the total number of flights for each month.
            flight_per_month_df = self._calculate_flights_per_month(flights_details_df)

            # Q2 Find the names of the 100 most frequent flyers.
            frequent_flyers_df = self._calculate_frequent_flyers(passenger_flight_df, passenger_details_df)

            # Q4 Find the passengers who have been on more than 3 flights together.
            co_passengers_df = self._calculate_co_passengers(passenger_flight_df)

            # Q5 Find the passengers who have been on more than N flights together within the range.
            co_passengers__more_than_n_df = self._calculate_co_passengers_more_than_n(flight_customer_df, 7, '2017-01-01', '2017-07-31')

            # store results in gold layer
            self._write_csv_to_gold(flight_per_month_df, f'{self.output_path}q1_flight_per_month')
            self._write_csv_to_gold(frequent_flyers_df, f'{self.output_path}q2_frequent_flyers')
            self._write_csv_to_gold(co_passengers_df, f'{self.output_path}q4_more_than_3_flights_together')
            self._write_csv_to_gold(co_passengers__more_than_n_df, f'{self.output_path}q5_more_than_n_flights_together_in_range')

        except Exception as e:
            self.log.error(f'An error occurred: {e}')
            raise


if __name__ == '__main__':
    session = get_spark_session("Flight Analysis")
    fa = FlightAnalysis(session)
    fa.main()
    stop_spark_session()