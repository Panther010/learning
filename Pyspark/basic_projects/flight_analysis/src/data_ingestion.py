from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logger


class FlightIngest:

    def __init__(self) -> None:
        self.spark = SparkSession.builder.appName('flight Ingest').master('local').getOrCreate()

        self.flight_raw_file = '../../../input_data/raw/flightData.csv'
        self.passenger_raw_file = '../../../input_data/raw/passengers.csv'

        self.output_path = '../../../input_data/silver/'

        self.log = logger.setup_logger()

    def _read_csv_data(self, file_path: str) -> DataFrame:
        self.log.info(f'reading data from {file_path}')
        return self.spark.read.csv(file_path, inferSchema=True, header=True)

    @staticmethod
    def camel_to_snake_case(col: str) -> str:
        new_col = ''.join([f'_{char.lower()}' if char.isupper() else char for char in col]).lstrip('_')
        return new_col

    def _write_parquet_to_bronze(self, df:DataFrame, file_path: str) -> None:
        self.log.info(f'writing data to {file_path}')
        columns = [self.camel_to_snake_case(col) for col in df.columns]
        df = df.toDF(*columns)
        df.coalesce(1).write.option("compression", "snappy").mode("overwrite").parquet(file_path)

    def _normalise_data(self, flights:DataFrame) -> tuple[DataFrame, DataFrame]:
        self.log.info(f'Data normalisation is in progress')
        passenger_flight = flights.select(f.col('passengerId'), f.col('flightId'))
        flight_details = flights.select(f.col('flightId'), f.col('from'), f.col('to'), f.col('date')).dropDuplicates()
        return passenger_flight, flight_details

    def main(self) -> None:
        try:
            flight_df = self._read_csv_data(self.flight_raw_file).cache()

            passenger_flight_df, flight_details_df = self._normalise_data(flight_df)

            passenger_df = self._read_csv_data(self.passenger_raw_file)

            self._write_parquet_to_bronze(flight_df, f'{self.output_path}flights_data')
            self._write_parquet_to_bronze(passenger_df, f'{self.output_path}passenger_details')
            self._write_parquet_to_bronze(passenger_flight_df, f'{self.output_path}passenger_flight')
            self._write_parquet_to_bronze(flight_details_df, f'{self.output_path}flight_details')

        except Exception as e:
            self.log.error(f'An error occurred: {e}')
            raise
        finally:
            if self.spark is not None:
                self.spark.stop()


if __name__ == '__main__':
    fi = FlightIngest()
    fi.main()