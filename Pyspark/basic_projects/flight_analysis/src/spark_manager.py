from pyspark.sql import SparkSession

def get_spark_session(app_name="Flight Analysis"):
    """
    Creates or retrieves the existing SparkSession.
    Ensures only one session is used across all scripts.
    """
    spark = SparkSession.getActiveSession()
    if spark is None:  # Create session only if none exists
        spark = SparkSession.builder.appName(app_name).getOrCreate()
    return spark

def stop_spark_session():
    """Stops the active SparkSession if running standalone."""
    spark = SparkSession.getActiveSession()
    if spark is not None:
        spark.stop()
