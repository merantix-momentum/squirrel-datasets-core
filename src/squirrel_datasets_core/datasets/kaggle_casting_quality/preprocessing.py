from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

from squirrel_datasets_core.datasets.kaggle_casting_quality.driver import RawKaggleCastingQuality
from squirrel_datasets_core.preprocessing.save_shards import SaveShardsConfig, save_shards
from squirrel_datasets_core.spark.setup_spark import get_spark


@dataclass
class KaggleCastingShardConfig(SaveShardsConfig):
    identifier: str = "kaggle_casting_quality"
    version: int = 1
    num_shards: int = 100
    output_data_url: str = "kaggle_casting_quality/train"
    output_catalog_url: str = "kaggle_casting_quality/train.yaml"
    split: str = "train"
    parse: bool = False


cs = ConfigStore.instance()
cs.store(name="kaggle_casting_config", node=KaggleCastingShardConfig)


@hydra.main(config_path=None, config_name="kaggle_casting_config")
def main(cfg: KaggleCastingShardConfig) -> None:
    """When running via cli create spark session yourself"""
    save_shards(
        cfg=cfg,
        session=get_spark("kagglecastingquality-preprocessing"),
        iter_kwargs=dict(split=cfg.split, parse=cfg.parse),
        hooks=[RawKaggleCastingQuality.load_sample],
    )


if __name__ == "__main__":
    main()
