# Pin the Debian release as well as Python. The unqualified `slim` tag moved to
# Debian Trixie, where the Java 17 package used below is unavailable. Bookworm
# provides Java 17 and makes this learning environment more reproducible.
FROM python:3.11-slim-bookworm

# Spark runs on the Java Virtual Machine, so a Java runtime is required even
# though the jobs themselves are written in Python. `--no-install-recommends`
# keeps the learning image focused and smaller.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Pin PySpark so every machine runs the same Spark version. This agrees with
# the repository's pyproject.toml requirement and avoids surprise upgrades.
RUN pip install --no-cache-dir pyspark==3.5.0

# This is the container's working directory. In a later phase, `spark_jobs/`
# will be mounted here so the container can run your local job files.
WORKDIR /opt/spark-jobs

# `docker run <image>` prints the installed Python version unless a command is
# supplied after the image name, e.g. `spark-submit /opt/spark-jobs/job.py`.
CMD ["python", "--version"]
