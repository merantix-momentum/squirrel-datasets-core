from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

from pyspark.sql import SparkSession
from squirrel.catalog import Catalog, Source
from squirrel.serialization import MessagepackSerializer
from squirrel.store import SquirrelStore
from pyspark import TaskContext

if TYPE_CHECKING:
    from squirrel.constants import ShardType
    from squirrel.iterstream import Composable
    from squirrel.store import AbstractStore

@dataclass
class SaveShardsConfig:
    identifier: str  # identifier used in the catalog for the dataset
    version: int  # dataset version to use
    num_shards: int
    output_data_url: str  # path where the shard will be written
    output_catalog_url: str  # path where the catalog will be written
    num_samples: Optional[int] = None  # number of samples to take from the dataset, if None, all samples will be taken


def save_iterable_as_shard(shard: ShardType, store: AbstractStore) -> None:
    """Helper to save a single shard into a messagepack store using squirrel"""
    store.set(key=f"shard_{TaskContext.get().partitionId()}", value=list(shard))


def save_composable_to_shards(
    src_it: Composable,
    session: SparkSession,
    out_url: str,
    num_samples: int,
    num_shards: int,
    hooks: Optional[List[Callable[[Dict], Dict]]] = None,
    save_catalog: Optional[bool] = False,
    catalog_identifier: Optional[str] = "",
    catalog_version: Optional[int] = 1,
    catalog_output_url: Optional[str] = "",
) -> None:
    """Save single iterstream to messagepack."""
    if num_samples is not None:
        src_it = src_it.take(num_samples)

    store = SquirrelStore(out_url, serializer=MessagepackSerializer())
    pipe = session.sparkContext.parallelize(src_it)
    for h in hooks:
        pipe = pipe.map(h)
    pipe = pipe.coalesce(num_shards)
    _ = pipe.foreachPartition(partial(save_iterable_as_shard, store=store))

    if save_catalog:
        ncat = Catalog()
        # set version via DummyCatalogSource
        cat_source = ncat[catalog_identifier]
        cat_source[catalog_version + 1] = Source(
            driver_name="messagepack",
            driver_kwargs={"url": out_url},
        )
        ncat.to_file(catalog_output_url)


def save_source_to_shards(
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

    save_composable_to_shards(src_it, session, cfg.output_data_url, cfg.num_samples, cfg.num_shards, hooks,
                              save_catalog=True, catalog_identifier=cfg.identifier, catalog_version=cfg.version, 
                              catalog_output_url=cfg.output_catalog_url)
