from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging


class CardsInsights:

    def __init__(self):

        self.spark = SparkSession.builder.appName('cards and loans').master('local').getOrCreate()

        self.cards_input = '../../../input_data/bronze/credit-card'
        self.loans_input = '../../../input_data/silver/loans'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')

    def data_reader(self, file_path: str) -> DataFrame:
        self.log.info(f'Reading data from {file_path} ..')
        return self.spark.read.parquet(file_path)

    def eligible_for_cards(self, card_df: DataFrame) -> DataFrame:
        """
        User fulfilling fllowing criteria will be eligible for cards
            1. Salary more than 50000
            2. Age more than 18 years
            3. Credit score more than 650
        """
        eligible_users = card_df.filter((f.col('credit_score') > f.lit(650)) &
                                        (f.col('age') > f.lit(18)) &
                                        (f.col('estimated_salary') > f.lit(50000)))

        self.log.info(f' User count eligible for cards is {eligible_users.count()} \n')
        return eligible_users

    def eligible_active_users(self, eligible_df: DataFrame) -> DataFrame:
        active_users = eligible_df.filter(f.col('is_active_member') == f.lit(1))
        self.log.info(f'User count who are active and eligible for card {active_users.count()} \n')
        return active_users

    def targeted_users(self, active_eligible_df: DataFrame) -> DataFrame:
        target = active_eligible_df.filter(f.col('balance') >= f.lit(25000))
        self.log.info(f'User can be targeted for cards {target.count()} \n')
        return active_eligible_df

    def less_tenure(self, targeted_df: DataFrame) -> DataFrame:
        tenure_filter = targeted_df.filter(f.col('tenure') < f.lit(5))
        self.log.info(f'Count of targeted user with tenure less than 5 is {tenure_filter.count()} \n')
        return tenure_filter

    def exited_users(self, targeted_df: DataFrame) -> DataFrame:
        exited_filter = targeted_df.filter(f.col('exited') == f.lit(1))
        self.log.info(f'Count of targeted user who exited is {exited_filter.count()} \n')
        return exited_filter

    def product_check(self, targeted_df: DataFrame) -> DataFrame:
        single_product = targeted_df.filter(f.col('num_of_products') == f.lit(1))
        self.log.info(f'Count of targeted users with single product {single_product.count()} \n')
        return single_product

    def spain_user(self, cards_df: DataFrame) -> DataFrame:
        spain_card_users = cards_df.filter(f.lower(f.col('geography')) == f.lit('spain'))
        self.log.info(f'Count of cards users in spain is {spain_card_users.count()} \n')
        return spain_card_users

    def low_salary_user(self, cards_df: DataFrame) -> DataFrame:
        low_salary_users = cards_df.filter((f.col('estimated_salary') < f.lit(100000)) &
                                           (f.col('num_of_products') > f.lit(1)))
        self.log.info(f'Count of cards users estimated salary is less than 1 lakh and number of products '
                      f'more than 1 is : {low_salary_users.count()} \n')
        return cards_df

    def main(self):
        loans = self.data_reader(self.loans_input)
        loans.printSchema()
        cards = self.data_reader(self.cards_input)
        cards.printSchema()

        eligible = self.eligible_for_cards(cards)
        active = self.eligible_active_users(eligible)
        targeted = self.targeted_users(active)
        tenure = self.less_tenure(targeted)
        exited = self.exited_users(targeted)
        product = self.product_check(targeted)
        spain = self.spain_user(cards)
        low_salary = self.low_salary_user(cards)


if __name__ == '__main__':
    ci = CardsInsights()
    ci.main()
