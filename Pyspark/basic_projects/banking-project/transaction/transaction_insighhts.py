from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging

class TransactionInsights:

    def __init__(self):
        self.spark = SparkSession.builder.appName('cards and loans').master('local').getOrCreate()

        self.input_path = '../../../input_data/silver/transaction'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def data_reader(self, file_path: str) -> DataFrame:
        self.log.info(f'Reading data from {file_path} ..')
        return self.spark.read.parquet(file_path)

    def main(self):
        tx_data = self.data_reader(self.input_path)
        tx_data.printSchema()
        print(tx_data.count())


if __name__ == '__main__':
    ti = TransactionInsights()
    ti.main()