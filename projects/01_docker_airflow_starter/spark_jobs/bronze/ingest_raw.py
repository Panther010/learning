from pyspark.sql import DataFrame
from pathlib import Path
from pyspark.sql import functions as f
from shared.path_utils import get_processed_data_dir, get_raw_data_dir
from shared.logger import get_logger
from shared.spark_session import get_or_create_spark, stop_spark


class RawIngest:
    def __init__(self) -> None:
        self.spark = get_or_create_spark(app_name="olympic-bronze-ingestion")

        raw_dir = get_raw_data_dir() / "olympic" / "2022"

        self.athletes_file = raw_dir / "olympic_athletes.csv"
        self.host_file = raw_dir / "olympic_hosts.csv"
        self.medal_file = raw_dir / "olympic_medals.csv"
        self.result_file = raw_dir / "olympic_results.csv"

        self.output_path = get_processed_data_dir() / "olympic_2022" / "bronze"

        self.log = get_logger(__name__)

    def read_file(self, path:Path) -> DataFrame:
        self.log.info(f"reading file {path}")
        return self.spark.read.csv(str(path), header=True, multiLine=True, escape='"')

    def write_data(self, df:DataFrame, table_name:str) -> None:
        self.log.info(f"Writing data in table {self.output_path}/{table_name}")
        full_path = f"{self.output_path}/{table_name}"
        final_data = df.withColumn("_ingested_at", f.current_timestamp()) \
                      .withColumn("_source_file", f.input_file_name())
        final_data.show()
        final_data.write.parquet(full_path, mode='overwrite')

    def main(self) -> None:
        self.log.info(f'Starting to run the JOB')
        athletes_df = self.read_file(self.athletes_file)
        host_df = self.read_file(self.host_file)
        medal_df = self.read_file(self.medal_file)
        result_df = self.read_file(self.result_file)
        athletes_df.printSchema()
        print(athletes_df.count())
        host_df.printSchema()
        print(host_df.count())
        medal_df.printSchema()
        print(medal_df.count())
        result_df.printSchema()
        print(result_df.count())
        self.write_data(athletes_df, "olympic_athletes")
        self.write_data(host_df, "olympic_hosts")
        self.write_data(medal_df, "olympic_medals")
        self.write_data(result_df, "olympic_results")


if __name__ == '__main__':
    ingest = RawIngest()
    ingest.main()
    stop_spark()