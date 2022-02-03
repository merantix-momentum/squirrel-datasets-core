import os
from dataclasses import dataclass
from functools import partial
from typing import Callable, Dict, Iterable, List, Optional

from pyspark.sql import SparkSession
from squirrel.catalog import Catalog, Source
from squirrel.driver.messagepack.msgstore import MessagepackStore
from squirrel.driver.spec import Sample, Shard


@dataclass
class SaveShardsConfig:
    identifier: str  # identifier used in the catalog for the dataset
    version: int  # dataset version to use
    num_shards: int
    output_data_url: str  # path where the shard will be written
    output_catalog_url: str  # path where the catalog will be written
    num_samples: Optional[int] = None  # number of samples to take from the dataset, if None, all samples will be taken


def save_iterable_as_shard(pt: Iterable, output_url: str) -> None:
    """Helper to save a shard into a messagepack store using squirrel"""
    pt = list(pt)
    if len(pt) == 0:
        return
    store = MessagepackStore(output_url)
    store.set(Shard(pt))


def save_shards(
    cfg: SaveShardsConfig,
    session: SparkSession,
    iter_kwargs: Dict,
    hooks: Optional[List[Callable[[Dict], Dict]]] = None,
) -> None:
    """Process a source and save it as messagepack.

    Args:
        cfg (SaveShardsConfig): Config to use.
        session (SparkSession): Spark session.
        iter_kwargs (Dict): Keyword arguments passed to :py:meth:`Driver.get_iter`.
        hooks (Optional[List[Callable[[Dict], Dict]]], optional): Methods to map to the samples before creating shards.
    """
    if hooks is None:
        hooks = []

    # get raw data
    cat = Catalog.from_plugins()
    d = cat[cfg.identifier][cfg.version]
    src_it = d.load.get_iter(**iter_kwargs)
    if cfg.num_samples is not None:
        src_it = src_it.take(cfg.num_samples)

    # resolve relative paths
    out_url = os.path.abspath(cfg.output_data_url)

    # run preprocessing with spark
    pipe = session.sparkContext.parallelize(src_it)
    for h in hooks:
        pipe = pipe.map(h)
    pipe = pipe.map(Sample)
    pipe = pipe.coalesce(cfg.num_shards)
    _ = pipe.foreachPartition(partial(save_iterable_as_shard, output_url=out_url))

    ncat = Catalog()
    # set version via DummyCatalogSource
    cat_source = ncat[cfg.identifier]
    cat_source[cfg.version + 1] = Source(
        driver_name="messagepack",
        metadata=d.metadata,
        driver_kwargs={"url": out_url},
    )
    ncat.to_file(cfg.output_catalog_url)
