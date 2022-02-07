from dataclasses import asdict, dataclass

import hydra
from hydra.core.config_store import ConfigStore

from squirrel_datasets_core.datasets.ds_bowl_2018.driver import DataScienceBowl2018Driver
from squirrel_datasets_core.preprocessing.save_shards import SaveShardsConfig, save_shards
from squirrel_datasets_core.spark.setup_spark import get_spark


@dataclass
class IterKwargs:
    split: str = "stage1_train"
    parse_image: bool = False
    parse_mask: bool = False
    shuffle_size: int = 50
    shuffle_initial: int = 50


@dataclass
class DsBowlShardConfig(SaveShardsConfig):
    identifier: str = "ds_bowl_18"
    version: int = 1
    num_shards: int = 100
    output_data_url: str = "/data/ds_bowl_shards"
    output_catalog_url: str = "/data/ds_bowl_shards/shards.yaml"
    iter_kwargs: IterKwargs = IterKwargs()


cs = ConfigStore.instance()
cs.store(name="ds_bowl_18_config", node=DsBowlShardConfig)


@hydra.main(config_path=None, config_name="ds_bowl_18_config")
def main(cfg: DsBowlShardConfig) -> None:
    """When running via cli create spark session yourself"""
    save_shards(
        cfg=cfg,
        session=get_spark("ds-bowl-18-preprocessing"),
        iter_kwargs=asdict(cfg.iter_kwargs),
        hooks=[DataScienceBowl2018Driver.load_sample],
    )


if __name__ == "__main__":
    main()
