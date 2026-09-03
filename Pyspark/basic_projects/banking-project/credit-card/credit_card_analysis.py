from shared.logger import get_logger
from shared.path_utils import get_project_root, get_data_dir, get_raw_data_dir, get_processed_data_dir
from shared.spark_session import get_or_create_spark, stop_spark

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql import DataFrame


class CreditCardAnalysis:

    def __init__(self):
        self.spark = get_or_create_spark()
        self.raw_dir = get_raw_data_dir() / 'banking/credit_card.csv'

        print(self.raw_dir)
        self.log = get_logger(__name__)

    def read_data(self) -> DataFrame:
        raw_df = self.spark.read.format("csv").option("header", True).option("inferSchema", True).load(str(self.raw_dir))
        raw_df.printSchema()
        return raw_df

    def camel_to_snake_case(self, column_name: str) -> str:
        """
        Converts a CamelCase string to snake_case.
        """
        return ''.join(['_' + char.lower() if char.isupper() else char for char in column_name]).lstrip('_')


    def correct_column_names(self, input_df: DataFrame) -> DataFrame:
        """
        Converts all column names in the input DataFrame to snake_case.
        """
        new_col = [self.camel_to_snake_case(col).strip() for col in input_df.columns]
        new_df = input_df.toDF(*new_col)
        return new_df

    def eligible_for_cards(self, card_df: DataFrame) -> DataFrame:
        """
        User fulfilling fllowing criteria will be eligible for cards
            1. Salary more than 50000
            2. Age more than 18 years
            3. Credit score more than 650
        """
        self.log.info(f"calculating eligible customers")
        result = card_df.filter(
            (F.col('estimated_salary') > F.lit(50000)) &
            (F.col('age') > F.lit(18)) &
            (F.col('credit_score') > F.lit(650))
        )

        return result

    def active_eligible_cust(self, eligible_cust: DataFrame) -> DataFrame:
        self.log.info(f"calculating the active customer from the list of eligible customers")
        result = eligible_cust.filter(
            F.col('is_active_member') == F.lit(1)
        )

        return result

    def potential_target(self, eligible_df: DataFrame) -> DataFrame:
        self.log.info(f"Customers having balance more than 25000 are potential customer")
        result = eligible_df.filter(
            F.col('balance') >= F.lit(25000)
        )

        return result

    def tenure_check(self, target_df:DataFrame) -> DataFrame:
        self.log.info(f'Count of targeted user with tenure less than 5 is ')

        result = target_df.filter(
            F.col('tenure') < F.lit(5)
        )

        return result

    def main(self):
        raw_credit_data = self.read_data()
        correct_df = self.correct_column_names(raw_credit_data)

        eligible_cust = self.eligible_for_cards(correct_df)
        print(eligible_cust.count())
        active_cust = self.active_eligible_cust(eligible_cust)
        print(active_cust.count())
        target_cust = self.potential_target(active_cust)
        print(target_cust.count())
        tenure_validation = self.tenure_check(target_cust)
        print(tenure_validation.count())


if __name__ == "__main__":
    cca = CreditCardAnalysis()
    cca.main()
    stop_spark()
