import os
import shutil
import logging
from pyspark.sql import SparkSession
from Pyspark.Streaming.jobs.batch_word_count import BatchWordCount


class BatchWCTester:

    def __init__(self):
        self.base_data_dir = '../Streaming/data'
        self.output_dir = '../Streaming/output/counter/'

        self.test_data_dir = '../datasets/'

        self.spark = SparkSession.builder.appName('Word Count tester').master('local').getOrCreate()

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(format=formatter, level=logging.INFO)
        self.log = logging.getLogger('logger')

    def clean_tests(self):

        # Clean output directory
        self.log.info(f"Starting to clean output directories")
        if os.path.exists(self.output_dir):
            self.log.info(f"List of files {os.listdir(self.output_dir)} ...\n")
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        # Clean input directory
        self.log.info(f"Starting to clean input directories")
        if os.path.exists(self.base_data_dir):
            self.log.info(f"List of files {os.listdir(self.base_data_dir)} ...\n")
            shutil.rmtree(self.base_data_dir)
        os.makedirs(self.base_data_dir, exist_ok=True)

    def ingest_data(self, itr):
        self.log.info(f"Starting to ingest data for iteration {itr}")
        source_file = os.path.join(self.test_data_dir, f"text_data_{itr}.txt")
        dest_file = os.path.join(self.base_data_dir)
        self.log.info(f"Copying file {source_file} to {dest_file}")

        shutil.copy(source_file, dest_file)

    def assert_results(self, expected_count):
        self.log.info(f"Starting to validate ")
        try:
            wc_df = self.spark.read.parquet(self.output_dir)
            wc_df.createOrReplaceTempView('wc')

            actual_count = self.spark.sql("select sum(count) from wc where word like 's%'").collect()[0][0]
            assert actual_count == expected_count , f"Test failed! Actual count: {actual_count}, Expected count: {expected_count}"
            self.log.info(f"Validation completed successfully. Actual count: {actual_count}, Expected count: {expected_count}")
        except Exception as e:
            self.log.info(f"Validation failed with error: {e}")

    def run_tests(self):
        self.clean_tests()

        wc = BatchWordCount(self.base_data_dir, self.output_dir, spark=self.spark)

        for itr, expected_count in zip([1, 2, 3], [25, 32, 37]):
            self.log.info(f"Starting to test itr {itr} of batch word count...")
            self.ingest_data(itr)
            wc.run()
            self.assert_results(expected_count)
            self.log.info(f"Iteration {itr} of batch word count completed.\n\n")


if __name__ == "__main__":
    test_suite = BatchWCTester()
    test_suite.run_tests()