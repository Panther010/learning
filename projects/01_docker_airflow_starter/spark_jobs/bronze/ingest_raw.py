from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from pyspark.sql.types import StringType, StructField, StructType

from shared.logger import get_logger
from shared.path_utils import get_processed_data_dir, get_raw_data_dir
from shared.spark_session import get_or_create_spark, stop_spark

CORRUPT_RECORD_COLUMN = "_corrupt_record"

RAW_COLUMN_NAMES = {
    "olympic_athletes.csv": [
        "athlete_url",
        "athlete_full_name",
        "games_participations",
        "first_game",
        "athlete_year_birth",
        "athlete_medals",
        "bio",
    ],
    "olympic_hosts.csv": [
        "game_slug",
        "game_end_date",
        "game_start_date",
        "game_location",
        "game_name",
        "game_season",
        "game_year",
    ],
    "olympic_medals.csv": [
        "discipline_title",
        "slug_game",
        "event_title",
        "event_gender",
        "medal_type",
        "participant_type",
        "participant_title",
        "athlete_url",
        "athlete_full_name",
        "country_name",
        "country_code",
        "country_3_letter_code",
    ],
    "olympic_results.csv": [
        "discipline_title",
        "event_title",
        "slug_game",
        "participant_type",
        "medal_type",
        "athletes",
        "rank_equal",
        "rank_position",
        "country_name",
        "country_code",
        "country_3_letter_code",
        "athlete_url",
        "athlete_full_name",
        "value_unit",
        "value_type",
    ],
}


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

    @staticmethod
    def build_raw_schema(column_names: list[str]) -> StructType:
        """Build an all-string Bronze schema and preserve parser-level bad rows."""
        fields = [StructField(column_name, StringType(), nullable=True) for column_name in column_names]
        fields.append(StructField(CORRUPT_RECORD_COLUMN, StringType(), nullable=True))
        return StructType(fields)

    def read_file(self, path: Path) -> DataFrame:
        self.log.info("reading file: %s", path)
        schema = self.build_raw_schema(RAW_COLUMN_NAMES[path.name])

        return (
            self.spark.read.option("header", True)
            .option("multiLine", True)
            .option("escape", '"')
            .option("mode", "PERMISSIVE")
            .option("columnNameOfCorruptRecord", CORRUPT_RECORD_COLUMN)
            .schema(schema)
            .csv(str(path))
        )

    def write_data(self, df: DataFrame, table_name: str) -> None:
        full_path = self.output_path / table_name
        self.log.info("Writing Bronze table %s to %s", table_name, full_path)

        final_data = df.withColumn("_ingested_at", f.current_timestamp()) \
                      .withColumn("_source_file", f.input_file_name())
        final_data.write.parquet(str(full_path), mode='overwrite')

    def main(self) -> None:
        athletes_df = self.read_file(self.athletes_file)
        host_df = self.read_file(self.host_file)
        medal_df = self.read_file(self.medal_file)
        result_df = self.read_file(self.result_file)

        self.write_data(athletes_df, "olympic_athletes")
        self.write_data(host_df, "olympic_hosts")
        self.write_data(medal_df, "olympic_medals")
        self.write_data(result_df, "olympic_results")


if __name__ == '__main__':
    ingest = RawIngest()
    try:
        ingest.main()
    finally:
        stop_spark()
