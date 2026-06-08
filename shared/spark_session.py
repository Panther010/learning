from pyspark.sql import SparkSession
from shared.logger import get_logger

logger = get_logger(__name__)

_spark: SparkSession | None = None

def get_or_create_spark(
        app_name: str = "Pyspark App",
        master: str = "local[*]",
        config: dict | None = None
) -> SparkSession:
    global _spark

    if _spark is None:

        logger.info("Creating new SparkSession: app=%s master=%s", app_name, master)
        builder = SparkSession.builder.appName(app_name).master(master)

        if config:
            for key, value in config.items():
                builder = builder.config(key, value)
                logger.debug("Spark config: %s = %s", key, value)

        _spark = builder.getOrCreate()
        logger.info("SparkSession created successfully")
    else:
        logger.debug("Returning existing SparkSession (app=%s)", _spark.sparkContext.appName)

    return _spark

def stop_spark() -> None:
    global _spark
    if _spark is not None:
        logger.info("Stopping SparkSession")
        _spark.stop()
        _spark = None
        logger.info("SparkSession stopped")
    else:
        logger.debug("stop_spark called but no active session exists")
