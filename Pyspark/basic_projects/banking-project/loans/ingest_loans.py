from pyspark.sql import SparkSession, DataFrame
import logging


class LoanIngest:
    """
    LoanIngest Class for Data Processing Pipeline
    =============================================
    This class handles the ingestion, processing, and saving of loan data.

    Functionalities:
    1. Read raw CSV loan data from a specified input path.
    2. Clean and standardize column names.
    3. Write the processed data into a Parquet format at the specified output path.
    """

    def __init__(self):
        """
        Initialize the LoanIngest class by setting up Spark session, input and output paths, and logger.
        """
        self.spark = SparkSession.builder.appName('loan ingest').master('local').getOrCreate()

        self.input_path = '../../../input_data/raw/loan.csv'
        self.output_path = '../../../input_data/bronze/loans'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def read_data(self):
        """
        Read the raw loan data from a CSV file into a Spark DataFrame.
        Returns:
            DataFrame: A PySpark DataFrame containing the raw loan data.
        """
        self.log.info(f'Starting the read the file')
        return self.spark.read.csv(self.input_path, inferSchema=True, header=True)

    def correct_column_names(self, raw_df: DataFrame) -> DataFrame:
        """
        Standardize column names by removing spaces, converting to lowercase, and replacing spaces with underscores.
        Args:
            raw_df (DataFrame): The raw DataFrame with original column names.
        Returns:
            DataFrame: A DataFrame with cleaned column names.
        """
        updated_col = [col.strip().lower().replace(' ', '_') for col in raw_df.columns]
        self.log.info(f"correcting the columns updated columns: {updated_col}")
        new_df = raw_df.toDF(*updated_col)
        new_df.printSchema()
        return new_df

    def write_data(self, data_df: DataFrame):
        """
        Write the processed DataFrame to a Parquet file.
        Args:
            data_df (DataFrame): The processed DataFrame to save.
        """
        data_df.write.parquet(self.output_path, mode='overwrite')

    def main(self):
        """
        Main pipeline to execute the ingestion, processing, and saving steps.
        """
        self.log.info('Pipeline execution started. \n')
        loans_df = self.read_data()
        column_corrected_df = self.correct_column_names(loans_df)
        self.write_data(column_corrected_df)

        # For development and debugging: Print schema, sample data, and record count.
        self.log.info('Displaying schema, sample data, and record count for verification...')
        # Delete these in case of actual project
        column_corrected_df.printSchema()
        column_corrected_df.show()
        self.log.info(f"Total record count: {column_corrected_df.count()} .\n")
        self.log.info('Pipeline execution completed successfully.')

        self.spark.stop()

# Entry point for the script
if __name__ == '__main__':
    ingest = LoanIngest()
    ingest.main()