from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging

"""
LoansClean Class for Data Cleaning Pipeline
===========================================
This class handles the cleaning and transformation of loan data.

Functionalities:
1. Read loan data from a Parquet file in the "bronze" stage.
2. Format and clean specific columns (e.g., remove commas, cast to decimal).
3. Fill missing values with defaults for specified columns.
4. Write the cleaned data into the "silver" stage in Parquet format.
"""


class LoansClean:
    """
    A class to manage the cleaning and transformation of loan data.
    """

    def __init__(self):
        """
        Initialize the LoansClean class by setting up Spark session, input and output paths, and logger.
        """
        self.spark = SparkSession.builder.appName('loan ingest').master('local').getOrCreate()

        self.input_path = '../../../input_data/bronze/loans'
        self.output_path = '../../../input_data/silver/loans'
        
        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def data_read(self):
        """
        Read the raw loan data from the Parquet file into a Spark DataFrame.
        Returns:
            DataFrame: A PySpark DataFrame containing the raw loan data.
        """
        self.log.info(f'Starting to read the data')
        return self.spark.read.parquet(self.input_path)

    def data_formatter(self, input_df: DataFrame) -> DataFrame:
        """
        Format specific columns by removing commas and casting to decimal type.
        Args:
            input_df (DataFrame): The raw DataFrame with original data.
        Returns:
            DataFrame: A DataFrame with formatted columns.
        """
        self.log.info('Formatting columns: loan_amount and debt_record...')
        return input_df \
            .withColumn('loan_amount',
                        f.regexp_replace(f.trim(f.col('loan_amount')), ',', '').cast('decimal(15,2)')) \
            .withColumn('debt_record',
                        f.regexp_replace(f.trim(f.col('debt_record')), ',', '').cast('decimal(15,2)'))

    def data_cleaner(self, formatted: DataFrame) -> DataFrame:
        """
        Clean the formatted data by filling missing values for specific columns.
        Args:
            formatted (DataFrame): The DataFrame with formatted columns.
        Returns:
            DataFrame: A cleaned DataFrame with missing values filled.
        """
        self.log.info('Cleaning data: Filling missing values in income and expenditure...')
        return formatted.fillna(0, ['income', 'expenditure'])

    def write_data(self, final_df: DataFrame):
        """
        Write the cleaned DataFrame to a Parquet file.
        Args:
            final_df (DataFrame): The cleaned DataFrame to save.
        """
        self.log.info(f'Writing cleaned data to: {self.output_path}')
        final_df.write.parquet(self.output_path, mode='overwrite')

    def main(self):
        """
        Main pipeline to execute the cleaning and transformation steps.
        """
        self.log.info('Pipeline execution started... \n')
        input_df = self.data_read()
        formatted_df = self.data_formatter(input_df)
        cleaned_df = self.data_cleaner(formatted_df)
        # For debugging: Print schema of the final DataFrame
        self.log.info('Displaying schema of the cleaned data for verification...')
        cleaned_df.printSchema()

        self.write_data(cleaned_df)
        self.log.info('Pipeline execution completed successfully.')

        self.spark.stop()


    # Entry point for the script
if __name__ == '__main__':
    lc = LoansClean()
    lc.main()
