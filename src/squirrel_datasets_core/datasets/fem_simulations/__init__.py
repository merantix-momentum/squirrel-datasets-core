from squirrel.catalog import CatalogKey, Source

__all__ = ["SOURCES"]
DRIVER_NAME = "messagepack"
METADATA = {"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"}

SOURCES = [
    (
        CatalogKey("GnnBvpEsTrainNoMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_train_no_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpEsTrainMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_train_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpEsValNoMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_val_no_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpEsValMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_val_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpEsTestShape", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_test_shape"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpEsTestSup", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_test_sup"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpMsTrainNoMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_train_no_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpMsTrainMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_train_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpMsValNoMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_val_no_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpMsValMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_val_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpMsTestShape", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_test_shape"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpMsTestSup", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_test_sup"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpElTrainNoMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElasticityFixedLineGenerator/norm_train_no_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpElTrainMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElasticityFixedLineGenerator/norm_train_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpElValNoMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElasticityFixedLineGenerator/norm_val_no_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpElValMa", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElasticityFixedLineGenerator/norm_val_ma"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpElTestShape", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElasticityFixedLineGenerator/norm_test_shape"
            },
            metadata=METADATA,
        ),
    ),
    (
        CatalogKey("GnnBvpElTestSup", 1),
        Source(
            driver_name=DRIVER_NAME,
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElasticityFixedLineGenerator/norm_test_sup"
            },
            metadata=METADATA,
        ),
    ),
]
