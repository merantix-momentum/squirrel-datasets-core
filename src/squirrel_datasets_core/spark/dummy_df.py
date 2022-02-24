from pyspark.sql import Row, SparkSession, DataFrame


def get_dummy_df(spark: SparkSession) -> DataFrame:
    """Returns a dummy dataframe."""
    return spark.sparkContext.parallelize(
        [
            Row(a="foo", b=1, c=5),
            Row(a="bar", b=2, c=6),
            Row(a="baz", b=3, c=None),
        ]
    ).toDF()
