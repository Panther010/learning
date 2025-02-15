from src.logger import setup_logger
from src.data_ingestion import FlightIngest
from src.flight_analysis import FlightAnalysis
from src.spark_manager import get_spark_session, stop_spark_session


class FlightAnalysisPipeline:

    def __init__(self):
        self.log = setup_logger()
        self.spark = get_spark_session("Flight analysis pipeline")

    def run(self):
        self.log.info("Running ingestion pipeline")
        ingest_data = FlightIngest(self.spark)
        ingest_data.main()
        self.log.info("Ingestion pipeline completed \n\n")

        self.log.info("Starting analysis")
        analysis = FlightAnalysis(self.spark)
        analysis.main()
        self.log.info("Analysis complete \n\n")

        stop_spark_session()


if __name__ == '__main__':
    flight_pipeline = FlightAnalysisPipeline()
    flight_pipeline.run()