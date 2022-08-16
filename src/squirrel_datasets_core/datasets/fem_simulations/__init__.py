# Exemplary sources for the huggingface driver

from squirrel.catalog import CatalogKey, Source

__all__ = ["SOURCES"]

SOURCES = [
    (
        CatalogKey("GnnBvpEsTrainNoMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_train_no_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpEsTrainMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_train_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpEsValNoMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_val_no_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpEsValMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_val_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpEsTestShape", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_test_shape"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpEsTestSup", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_test_sup"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpMsTrainNoMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_train_no_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpMsTrainMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_train_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpMsValNoMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_val_no_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpMsValMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_val_ma"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpMsTestShape", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_test_shape"
            },
        ),
    ),
    (
        CatalogKey("GnnBvpMsTestSup", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_test_sup"
            },
        ),
    ),
]
