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

    def account_transactions(self, transaction: DataFrame) -> DataFrame:
        self.log.info(f'Calculating Count of transactions on every account')
        result = transaction.groupby('account_no').agg(f.count(f.col('account_no')).alias('transaction_count'))
        result.show()
        return result

    def amount_withdraw(self, transaction: DataFrame) -> DataFrame:
        self.log.info(f'Calculating Maximum and Minimum withdrawal amount of an account')
        result = transaction.groupby('account_no').agg(f.max(f.col('withdrawal_amt')).alias('max_withdraw'),
                                                       f.min(f.col('withdrawal_amt')).alias('min_withdraw'))
        result.show()
        return result

    def amount_deposit(self, transaction: DataFrame) -> DataFrame:
        self.log.info(f'Calculating Maximum and Minimum deposit amount of an account')
        result = transaction.groupby('account_no').agg(f.max(f.col('deposit_amt')).alias('max_deposit'),
                                                       f.min(f.col('deposit_amt')).alias('min_deposit'))
        result.show()
        return result

    def account_balance(self, transaction: DataFrame) -> DataFrame:
        self.log.info(f'Calculating Sum of balance in every bank account')
        result = transaction.groupby('account_no').agg(f.sum(f.col('balance_amt')).alias('account_balance'))
        result.show()
        return result

    def transaction_methods(self, transaction: DataFrame) -> DataFrame:
        self.log.info(f'Calculating Count of transaction methods customers used')
        result = transaction.groupby('transaction_details').agg(f.count(f.col('account_no')).alias('tx_count'))
        result.show()
        return result

    def transaction_each_date(self, transaction: DataFrame) -> DataFrame:
        self.log.info(f'Calculating Number of transactions on each date')
        result = transaction.groupby('value_date').agg(f.count(f.col('account_no')).alias('tx_by_date_count'))
        result.show()
        return result

    def cust_list(self, transaction: DataFrame) -> DataFrame:
        self.log.info(f'Calculating List of customers with withdrawal amount more than 1 lakh')
        result = transaction.filter(f.col('withdrawal_amt') > f.lit(100000))
        result.show()
        return result

    def main(self):
        tx_data = self.data_reader(self.input_path)
        tx_data.printSchema()
        tx_data.show()
        act_txn = self.account_transactions(tx_data)
        max_min_withdraw = self.amount_withdraw(tx_data)
        max_min_deposit = self.amount_deposit(tx_data)
        acc_balance = self.account_balance(tx_data)
        txn_methods = self.transaction_methods(tx_data)
        tx_on_date = self.transaction_each_date(tx_data)
        customer_lis = self.cust_list(tx_data)


if __name__ == '__main__':
    ti = TransactionInsights()
    ti.main()