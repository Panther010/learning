from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging


class CreditCardIngest:

    def __init__(self):

        self.spark = SparkSession.builder.appName('credit_card_ingest').master('local').getOrCreate()

        # Define Input and Output Paths
        self.input_path = '../../../input_data/raw/credit_card.csv'
        self.output_path = '../../../input_data/bronze/credit-card'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def data_read(self) -> DataFrame:
        """
        Reads data from the input CSV file.
        """
        self.log.info(f'reading data from {self.input_path}')
        return self.spark.read.csv(self.input_path, inferSchema=True, header=True)

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
        self.log.info(f'correcting the column names from {input_df.columns} to {new_col}')
        new_df = input_df.toDF(*new_col)
        return new_df

    def write_data(self, raw_df: DataFrame) -> None:
        """
        Writes the processed DataFrame to the output path in Parquet format.
        """
        raw_df.write.parquet(self.output_path, mode='overwrite')

    def main(self):
        self.log.info(f'Starting to run the JOB')
        credit_card = self.data_read()
        updated_card = self.correct_column_names(credit_card)
        self.write_data(updated_card)

        self.log.info(f'Successfully completed the processing')



if __name__ == '__main__':
    cci = CreditCardIngest()
    cci.main()
