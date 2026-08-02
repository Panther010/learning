from pyspark.sql import DataFrame, Column
from pyspark.sql import functions as f

from shared.logger import get_logger
from shared.path_utils import get_processed_data_dir
from shared.spark_session import get_or_create_spark, stop_spark

class CleanAthlete:

    def __init__(self) -> None:
        self.spark = get_or_create_spark(app_name="athlete silver processing")

        process_dir = get_processed_data_dir()

        self.input_path = process_dir / 'olympic_2022' / 'bronze' / 'olympic_athletes'
        self.output_path = process_dir / 'olympic_2022' / 'silver' / 'olympic_athletes'

        self.log = get_logger(__name__)

    def read_data(self) -> DataFrame:
        self.log.info("reading file: %s", self.input_path)
        return self.spark.read.parquet(str(self.input_path))

    def deduplicate_data(self, df: DataFrame) -> DataFrame:
        self.log.info("removing duplicate from data")

        name_variant_df = df.groupby(f.col('athlete_url')).agg(
            f.sort_array(f.collect_set("athlete_full_name")).alias("athlete_name_variants"),
            f.first(f.col("games_participations"), ignorenulls=True).alias("games_participations"),
            f.first(f.col("first_game"), ignorenulls=True).alias("first_game"),
            f.first(f.col("athlete_year_birth"), ignorenulls=True).alias("athlete_year_birth"),
            f.first(f.col("athlete_medals"), ignorenulls=True).alias("athlete_medals"),
            f.first(f.col("bio"), ignorenulls=True).alias("bio"),
            f.first(f.col("_ingested_at"), ignorenulls=True).alias("_ingested_at"),
            f.first(f.col("_source_file"), ignorenulls=True).alias("_source_file"),
        ).withColumn(
            "athlete_full_name", f.element_at(f.col("athlete_name_variants"), 1)
        ).withColumn(
            "athlete_name_variant_count", f.size("athlete_name_variants")
        )

        return name_variant_df

    def medal_count(self, column_name: str, medal_code: str) -> Column:
        extracted = f.regexp_extract(
            f.col(column_name), rf"(?i)(\d+)\s*{medal_code}\b", 1
        )

        return f.when(extracted == "", f.lit(0)).otherwise(extracted.cast("int"))

    def correct_data_type(self, df: DataFrame) -> DataFrame:
        self.log.info("calculating medal details")
        result_df = df.select(
            f.col("athlete_url"),
            f.col("athlete_full_name"),
            f.col("games_participations").cast("int").alias("games_participations"),
            f.col("first_game"),
            f.col("athlete_year_birth").cast("int").alias("athlete_year_birth"),
            f.col("athlete_medals").alias("athlete_medals_raw"),
            f.trim(f.regexp_replace(f.coalesce(f.col("athlete_medals"), f.lit(" ")),
                                               r"\s+", " ")).alias("athlete_medals_clean"),
            f.col("athlete_name_variants"),
            f.col("athlete_name_variant_count"),
            f.col("bio"),
            f.col("_ingested_at"),
            f.col("_source_file")
        )

        self.log.info("calculating gold, silver and bronze medals for athlete separately and total medals")
        medals_df = result_df.withColumn("gold_medals", self.medal_count("athlete_medals_clean", "G")) \
            .withColumn("silver_medals", self.medal_count("athlete_medals_clean", "S")) \
            .withColumn("bronze_medals", self.medal_count("athlete_medals_clean", "B")) \
            .withColumn("total_medals", f.col("gold_medals") + f.col("silver_medals") + f.col("bronze_medals"))


        return medals_df

    def write_silver(self, df: DataFrame):
        df.coalesce(1).write.mode("overwrite").parquet(str(self.output_path))

    def main(self) -> None:

        athlete_df = self.read_data()

        dedup_athlete = self.deduplicate_data(athlete_df)

        silver_df = self.correct_data_type(dedup_athlete)
        self.write_silver(silver_df)
        # Note: there are few athlete without birt year of missing first game value keep in mind
        athlete_df.filter(f.col("athlete_year_birth").isNull() | f.trim(f.col("athlete_year_birth") == f.lit(""))).show()
        athlete_df.filter(
            f.col("games_participations").isNull() | f.trim(f.col("games_participations") == f.lit(""))).show()
        athlete_df.filter(
            f.col("first_game").isNull() | f.trim(f.col("first_game") == f.lit(""))).show()

        silver_df.filter(f.col("athlete_full_name").isin(["Evgeni SEMENENKO", "Mari EDER"])).show()

        print(silver_df.count())

if __name__ == '__main__':
    clean_athlete = CleanAthlete()
    try:
        clean_athlete.main()
    finally:
        stop_spark()
