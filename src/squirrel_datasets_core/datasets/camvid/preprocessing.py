from dataclasses import asdict, dataclass

import hydra
from hydra.core.config_store import ConfigStore

from squirrel_datasets_core.datasets.camvid.driver import CamvidDriver
from squirrel_datasets_core.preprocessing.save_shards import SaveShardsConfig, save_shards
from squirrel_datasets_core.spark.setup_spark import get_spark


@dataclass
class IterKwargs:
    split: str = "train"
    parse_image: bool = False
    parse_label: bool = False
    shuffle_size: int = 800
    shuffle_initial: int = 800


@dataclass
class CamvidShardConfig(SaveShardsConfig):
    identifier: str = "camvid"
    version: int = 1
    num_shards: int = 5
    output_data_url: str = "/data/camvid_shards"
    output_catalog_url: str = "/data/camvid_shards/shards.yaml"
    iter_kwargs: IterKwargs = IterKwargs()


cs = ConfigStore.instance()
cs.store(name="camvid_config", node=CamvidShardConfig)


@hydra.main(config_path=None, config_name="camvid_config")
def main(cfg: CamvidShardConfig) -> None:
    """When running via cli create spark session yourself"""
    save_shards(
        cfg=cfg,
        session=get_spark("camvid-preprocessing"),
        iter_kwargs=asdict(cfg.iter_kwargs),
        hooks=[CamvidDriver.load_sample],
    )


if __name__ == "__main__":
    main()
