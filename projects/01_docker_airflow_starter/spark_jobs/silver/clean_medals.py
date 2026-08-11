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

    def trim_string_col(self, df: DataFrame) -> DataFrame:
        self.log.info("Trim of all the string column is in progress")
        string_cols = [c for c, t in df.dtypes if t == "string"]
        for col_name in string_cols:
            df = df.withColumn(col_name, f.trim(f.col(f"{col_name}")))

        return df

    def main(self):
        raw_medals = self.read_raw_data()

        raw_medals.printSchema()
        raw_medals.show(truncate=False)

        trim_text_df = self.trim_string_col(raw_medals)
        trim_text_df.printSchema()
        trim_text_df.show(truncate=False)

        trim_text_df.createOrReplaceTempView("trim_text_df")
        self.spark.sql("select distinct medal_type from trim_text_df").show(truncate=False)
        self.spark.sql("select count(distinct country_code) from trim_text_df").show(200, truncate=False)
        self.spark.sql("select count(distinct country_3_letter_code) from trim_text_df").show(200, truncate=False)
        self.spark.sql("select distinct participant_type from trim_text_df").show(truncate=False)
        self.spark.sql("select distinct slug_game from trim_text_df").show(truncate=False)




if __name__ == "__main__":
    cm = CleanMedals()
    cm.main()