from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging

class CleanTransactions:

    def __init__(self):
        self.spark = SparkSession.builder.appName('clean transaction').master('local').getOrCreate()

        self.input_path = '../../../input_data/bronze/transaction'
        self.output_path = '../../../input_data/silver/transaction'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def read_data(self) -> DataFrame:
        self.log.info(f'Starting to read the data')
        return self.spark.read.parquet(self.input_path)

    def clean_tfx_data(self, tfx_df: DataFrame) -> DataFrame:
        self.log.info('Cleaning data: cleaning data and filling missing values')
        result = tfx_df.withColumn('account_no',
                                   f.replace(f.col('account_no'), f.lit("'"), f.lit(""))) \
                  .withColumn('value_date', f.to_date(f.col('value_date'), "d-MMM-yy"))

        return result.fillna(0, ['withdrawal_amt', 'deposit_amt', 'balance_amt'])

    def write_data(self, result_df: DataFrame) -> None:
        self.log.info(f'Writing data to {self.output_path}')
        result_df.write.parquet(self.output_path, mode='overwrite')

    def main(self):
        tfx_data = self.read_data()
        clean_tfx = self.clean_tfx_data(tfx_data)
        self.write_data(clean_tfx)


if __name__ == '__main__':
    ct = CleanTransactions()
    ct.main()
