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
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpEsTrainMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_train_ma"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpEsValNoMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_val_no_ma"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpEsValMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_val_ma"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpEsTestShape", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_test_shape"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpEsTestSup", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator/norm_test_sup"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpMsTrainNoMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_train_no_ma"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpMsTrainMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_train_ma"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpMsValNoMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_val_no_ma"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpMsValMa", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_val_ma"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpMsTestShape", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_test_shape"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
    (
        CatalogKey("GnnBvpMsTestSup", 1),
        Source(
            driver_name="messagepack",
            driver_kwargs={
                "url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator/norm_test_sup"
            },
            metadata={"publisher": "Merantix Momentum", "paper url": "https://arxiv.org/abs/2206.14092"},
        ),
    ),
]
