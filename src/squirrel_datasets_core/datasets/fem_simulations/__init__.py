# Exemplary sources for the huggingface driver

from squirrel.catalog import CatalogKey, Source

__all__ = ["SOURCES"]

SOURCES = [
    (
        CatalogKey("ElectrostaticsFemData", 1),
        Source(
            driver_name="MessagepackDriver",
            driver_kwargs={"url": "gs://squirrel-core-public-data/gnn_bvp_solver/ElectricsRandomChargeGenerator"},
        ),
    ),
    (
        CatalogKey("MagnetostaticsFemData", 1),
        Source(
            driver_name="MessagepackDriver",
            driver_kwargs={"url": "gs://squirrel-core-public-data/gnn_bvp_solver/MagneticsRandomCurrentGenerator"},
        ),
    ),
]
