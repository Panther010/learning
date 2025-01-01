from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging

"""
LoansInsights Class for Analytical Insights on Loan Data
=========================================================

This class processes loan data stored in a parquet format and provides insights 
such as loan distribution by category and occupation, overdue checks, debt analysis, 
and more. It also allows saving processed data partitioned by loan category.

Methods:
- __init__: Initializes the Spark session and logging.
- read_data: Reads input data from the specified path.
- loan_on_category: Provides loan amount and count by category.
- loan_occupation: Provides loan amount and count by occupation.
- loan_amount: Counts loans with amounts greater than 100,000.
- overdue_check: Counts loans with overdue days greater than 5.
- less_debt: Counts loans with debt records less than 20,000.
- marital_status: Analyzes loans by marital status.
- returned_check: Analyzes customers with returned cheques and low income.
- writer: Writes data partitioned by a specified column.
- run_insights: Executes all insight-related methods.
- main: Orchestrates the workflow.
"""


class LoansInsights:

    def __init__(self):
        """
        Initializes the LoansInsights class.
        Sets up Spark session, input/output paths, and logging configuration.
        """
        self.spark = SparkSession.builder.appName('Loan analysis').master('local').getOrCreate()
        self.inpt_path = '../../../input_data/silver/loans'
        self.output_path = '../../../input_data/gold/loans'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def read_data(self):
        """
        Reads the loan data from the parquet file located at the input path.
        """
        self.log.info('Reading loan data from input path.')
        return self.spark.read.parquet(self.inpt_path)

    def loan_on_category(self, input_data: DataFrame):
        """
        Analyzes the total loan amount and count by loan category.
        """
        self.log.info('Analyzing loan data by category.')
        cat_amount = input_data.groupby(f.col('loan_category')).agg(
            f.sum(f.col('loan_amount')).alias('total_loan'),
            f.count(f.col('loan_amount')).alias('loan_count')) \
            .orderBy(f.col('total_loan').desc())
        cat_amount.show()

    def loan_occupation(self, input_data: DataFrame):
        """
        Analyzes the total loan amount and count by occupation.
        """
        self.log.info('Analyzing loan data by occupation.')
        occ_amount = input_data.groupby(f.col('occupation')).agg(
                f.sum(f.col('loan_amount')).alias('total_loan'),
                f.count(f.col('loan_amount')).alias('loan_count')) \
            .orderBy(f.col('total_loan').desc())
        occ_amount.show(50)

    def loan_amount(self, input_data: DataFrame):
        """
        Counts the number of loans with amounts greater than 100,000.
        """
        more_load_df = input_data.filter(f.col('loan_amount') > f.lit(100000))
        self.log.info(f'Loan count greater than 100000 ---> {more_load_df.count()} . .\n')

    def overdue_check(self, input_data: DataFrame):
        """
        Counts the number of loans with overdue days greater than 5.
        """
        overdue = input_data.filter(f.col('overdue') > f.lit(5))
        self.log.info(f'Overdue greater thank 5 ---> {overdue.count()} . .\n')

    def less_debt(self, input_data: DataFrame):
        """
        Counts the number of loans with debt records less than 20,000.
        """
        debt = input_data.filter(f.col('debt_record') < f.lit(20000))
        self.log.info(f'Debt less thank 20000 ---> {debt.count()} . .\n')

    def marital_status(self, input_data: DataFrame):
        """
        Analyzes the loan count and total amount based on marital status.
        """
        self.log.info(f'Loan count and amount as per marital status')
        marital = input_data.groupby(f.col('marital_status')).agg(
            f.count('customer_id').alias('loan_count'),
            f.sum('loan_amount').alias('loan_amount'))
        marital.show()

    def returned_check(self, input_data: DataFrame):
        """
        Counts the number of customers with 2 or more returned cheques and income below 50,000.
        """
        returned = input_data.filter((f.col('returned_cheque') >= f.lit(2)) & (f.col('income') < f.lit(50000)))
        self.log.info(f'Number of people with 2 or more returned cheques and income less than 50000 ---> {returned.count()} . .\n')

    def writer(self, input_df: DataFrame, col: str):
        """
        Writes the processed data to the output path, partitioned by the specified column.
        """
        input_df.coalesce(1).write.parquet(self.output_path, partitionBy=col, mode='overwrite')

    def run_insights(self, input_df):
        """
        Executes all analysis methods on the input data.
        """
        self.loan_on_category(input_df)
        self.loan_occupation(input_df)
        self.loan_amount(input_df)
        self.overdue_check(input_df)
        self.less_debt(input_df)
        self.marital_status(input_df)
        self.returned_check(input_df)

    def main(self):
        """
        Main function to orchestrate the data processing workflow.
        Reads the data, performs analysis, and writes the output.
        """
        input_df = self.read_data()
        input_df.printSchema()

        self.run_insights(input_df)

        self.writer(input_df, 'loan_category')

        self.spark.stop()


if __name__ == '__main__':
    li = LoansInsights()
    li.main()