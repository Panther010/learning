from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from shared.logger import get_logger
from shared.path_utils import get_processed_data_dir
from shared.spark_session import get_or_create_spark, stop_spark

class CleanHost:

    def __init__(self):
        self.spark = get_or_create_spark(app_name="clean_host")

        processed_dir = get_processed_data_dir()

        self.input_path = processed_dir/ "olympic_2022" / "bronze" / "olympic_hosts"
        self.output_path = processed_dir / 'olympic_2022' / 'silver' / 'olympic_hosts'

        self.log = get_logger(__name__)

    def read_raw_data(self) -> DataFrame:
        self.log.info("reading file: %s", self.input_path)
        return self.spark.read.parquet(str(self.input_path))

    def parse_data(self, df: DataFrame) -> DataFrame:
        self.log.info("Parsing the data and data type")
        result = df.select(
            f.col("game_slug").alias("slug_game"),
            f.to_date(f.to_timestamp(f.col("game_end_date"))).alias("game_end_date"),
            f.to_date(f.to_timestamp(f.col("game_start_date"))).alias("game_start_date"),
            f.col("game_location"),
            f.col("game_name"),
            f.col("game_season"),
            f.col("game_year").cast("int").alias("game_year"),
            f.col("_ingested_at"),
            f.col("_source_file")
        )
        return result

    def write_silver(self, df: DataFrame) -> None:
        df.coalesce(1).write.mode("overwrite").parquet(str(self.output_path))

    def main(self):
        raw_host = self.read_raw_data()

        raw_host.printSchema()
        print(raw_host.count())
        raw_host.show(100, truncate=False)

        parsed_host = self.parse_data(raw_host)

        parsed_host.printSchema()
        parsed_host.show(100, truncate=False)
        parsed_host.createOrReplaceTempView("parsed_host")
        self.spark.sql("select slug_game, game_name from parsed_host").show()
        self.spark.sql("select count(1) from parsed_host where game_season not in ('Summer', 'Winter') ").show()
        self.spark.sql("select count(*) from parsed_host where game_end_date > game_start_date").show()
        self.spark.sql("select count(distinct slug_game) from parsed_host").show()

        self.write_silver(parsed_host)


if __name__ == "__main__":
    ch = CleanHost()
    ch.main()
    stop_spark()