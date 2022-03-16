import os
import typing as t

from pyspark import SparkConf
from pyspark.sql import SparkSession


def get_spark(
    app_name: str,
    dataset_conf: t.Dict[str, str] = None,
    add_gcs_connector: bool = True,
    add_hadoop: bool = False,
    mem_size: str = "4g",
    n_master_cores: int = None,
) -> SparkSession:
    """
    Get a spark session for your operation.

    Args:
        app_name: The name of your spark session.
        dataset_conf: A dictionary containing configs for your runtime spark configs. Must be configs that can be
            altered after the creation of the spark session, otherwise will be complained by spark. A detailed list of
            viable options can be found here: https://spark.apache.org/docs/latest/configuration.html.
        add_gcs_connector: If true, will add shaded gcs-connector for hadoop3 and other related jar files to spark.
            It must be True in order for cloudbuild to work.
        add_hadoop: If true, will add hadoop native libs to spark lib path, such that spark can use native hadoop lib
            tools to compress and decompress zst files.
        mem_size: Memory size for the driver node.
        n_master_cores: Specify number of parallel threads directly.

    Returns:
        SparkSession
    """
    conf = SparkConf()
    conf.set("spark.executor.memory", mem_size)
    conf.set("spark.jars.repositories", "https://maven.google.com/")  # add google maven repo as extra jars lookup link.
    # add already installed jar files into path.
    _SPARK_HOME = _get_home("SPARK_HOME")
    _EXTRA_LIB_PATH = f"{_SPARK_HOME}/jars"
    conf.set("spark.driver.extraLibraryPath", _EXTRA_LIB_PATH)
    conf.set("spark.executor.extraLibraryPath", _EXTRA_LIB_PATH)

    if add_gcs_connector:
        conf = _add_gcs_connector(conf)

    if add_hadoop:
        conf = _add_native_hadoop(conf, extra_lib_path=_EXTRA_LIB_PATH)

    assert isinstance(app_name, str), ValueError("`app_name` accept string only.")

    if n_master_cores is not None:
        spark = (
            SparkSession.builder.master(f"local[{n_master_cores}]").appName(app_name).config(conf=conf).getOrCreate()
        )
    else:
        spark = SparkSession.builder.appName(app_name).config(conf=conf).getOrCreate()

    if dataset_conf:
        for key, value in dataset_conf.items():
            spark.conf.set(key, str(value))

    return spark


def _get_home(env_var: str) -> str:
    """Get home directories for e.g. spark, hadoop or other java lib homes."""
    _HOME = os.environ.get(env_var)
    assert _HOME is not None, EnvironmentError(f"Could not find '{env_var}' in current OS env.")
    return _HOME


def _add_gcs_connector(conf: SparkConf) -> SparkConf:
    """Add gcs-connector and related dependencies (jar files) to spark configuration."""
    _SPARK_HOME = _get_home("SPARK_HOME")
    GCS_CONNECTOR_JARS = {
        "spark.jars.packages": "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.2",
        "spark.hadoop.fs.AbstractFileSystem.gs.impl": "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS",
        "spark.hadoop.fs.gs.impl": "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem",
        "spark.hadoop.google.cloud.auth.service.account.enable": "true",
        "spark.jars": f"{_SPARK_HOME}/jars/gcs-connector-hadoop3-latest.jar",
    }
    for key, val in GCS_CONNECTOR_JARS.items():
        conf.set(key, val)
    return conf


def _add_native_hadoop(conf: SparkConf, extra_lib_path: str = None) -> SparkConf:
    """Link extra hadoop native libs to spark configuration, such that spark can use these libraries to do some specific
    IO works. Must be added when one does I/O with zstandard compressed files in spark. (The actual hadoop native libs
    are pre-installed in docker image `infrastructure/docker/Dockerfile.spark`.
    """
    _HADOOP_HOME = _get_home("HADOOP_HOME")
    if extra_lib_path is not None:
        extra_lib_path = f"{extra_lib_path}:{_HADOOP_HOME}/lib/native"
    else:
        extra_lib_path = f"{_HADOOP_HOME}/lib/native"
    conf.set("spark.driver.extraLibraryPath", extra_lib_path)
    conf.set("spark.executor.extraLibraryPath", extra_lib_path)
    return conf


def stop_spark(spark: SparkSession) -> None:
    """Stop a spark session in a graceful way."""
    spark.sparkContext._gateway.shutdown_callback_server()
    spark.stop()


if __name__ == "__main__":
    spark = get_spark("test")
