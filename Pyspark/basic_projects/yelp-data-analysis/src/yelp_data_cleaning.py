from pyspark.sql import SparkSession, DataFrame
from src.logger import setup_logger
from src.spark_manager import stop_spark_session, get_spark_session
from pyspark.sql import functions as f
from pyspark.sql.types import *

class YelpDataCleaning:

    def __init__(self, spark: SparkSession) -> None:

        self.spark = spark
        self.log = setup_logger()

        self.input_path = '../../../../../../../Bigdata_Data/yelp_data/'

        self.output_path = '../../../input_data/bronze/'

    @staticmethod
    def column_list(df: DataFrame) -> list[str]:
        df_col = df.columns
        nested_columns = []
        for i in df.schema.fields:
            if isinstance(i.dataType, StructType):
                df_col.remove(i.name)
                nested_columns.extend([f'{i.name}.{col.name}' for col in i.dataType.fields])

        df_col.extend(nested_columns)

        return df_col

    @staticmethod
    def camel_to_snake(col_name):
        return "".join(['_' + char if char.isupper() else char for char in col_name]).lstrip('_').lower()

    def read_json(self, path: str) -> DataFrame:
        df = self.spark.read.json(path)

        columns = self.column_list(df)

        new_df = df.select([f.col(column).alias(
            self.camel_to_snake(column.replace('.', '_'))) for column in columns])
        new_df.printSchema()

        return df

    def write_data_to_bronze(self, df: DataFrame, path :str) -> None:
        self.log.info(f'writing data to {path}')
        df.coalesce(1).write.option("compression", "snappy").mode("overwrite").parquet(path)

    def main(self) -> None:
        business_df = self.read_json(f'{self.input_path}yelp_academic_dataset_business.json')
        self.write_data_to_bronze(business_df, f'{self.output_path}business')

        checkin_df = self.read_json(f'{self.input_path}yelp_academic_dataset_checkin.json')
        self.write_data_to_bronze(checkin_df, f'{self.output_path}checkin')

        tip_df = self.read_json(f'{self.input_path}yelp_academic_dataset_tip.json')
        self.write_data_to_bronze(tip_df, f'{self.output_path}tip')

        user_df = self.read_json(f'{self.input_path}yelp_academic_dataset_user.json')
        self.write_data_to_bronze(user_df, f'{self.output_path}user')

        review_df = self.read_json(f'{self.input_path}yelp_academic_dataset_review.json')
        self.write_data_to_bronze(review_df, f'{self.output_path}review')


if __name__ == '__main__':
    session = get_spark_session()
    yc = YelpDataCleaning(session)
    yc.main()
    stop_spark_session()