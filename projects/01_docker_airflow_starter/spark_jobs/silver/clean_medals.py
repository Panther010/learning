from pyspark.sql import DataFrame, Column
from pyspark.sql import functions as f

from shared.logger import get_logger
from shared.path_utils import get_processed_data_dir
from shared.spark_session import get_or_create_spark, stop_spark


class CleanMedals:

    def __init__(self):
        self.spark = get_or_create_spark(app_name="clean_host")

        processed_dir = get_processed_data_dir()

        self.input_path = processed_dir / "olympic_2022" / "bronze" / "olympic_medals"
        self.output_path = processed_dir / 'olympic_2022' / 'silver' / 'olympic_medals'

        self.log = get_logger(__name__)

    def read_raw_data(self) -> DataFrame:
        return self.spark.read.parquet(str(self.input_path))

    def main(self):
        raw_medals = self.read_raw_data()

        raw_medals.printSchema()
        raw_medals.show(truncate=False)



if __name__ == "__main__":
    cm = CleanMedals()
    cm.main()