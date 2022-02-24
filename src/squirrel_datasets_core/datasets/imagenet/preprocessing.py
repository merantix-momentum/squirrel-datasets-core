from dataclasses import asdict, dataclass

import hydra
from hydra.core.config_store import ConfigStore

from squirrel_datasets_core.preprocessing.save_shards import SaveShardsConfig, save_shards
from squirrel_datasets_core.spark.setup_spark import get_spark


@dataclass
class RawImagenetIterKwargs:
    split: str = "train"
    parse: bool = False
    shuffle: bool = True
    buffer_size: int = 100_000


@dataclass
class RawImagenetShardConfig(SaveShardsConfig):
    identifier: str = "imagenet"
    version: int = 1
    num_shards: int = 100
    output_data_url: str = "imagenet/train"
    output_catalog_url: str = "imagenet/train.yaml"
    iter_kwargs: RawImagenetIterKwargs = RawImagenetIterKwargs()


cs = ConfigStore.instance()
cs.store(name="imagenet_config", node=RawImagenetShardConfig)


@hydra.main(config_path=None, config_name="kaggle_casting_config")
def main(cfg: RawImagenetShardConfig) -> None:
    """When running via cli create spark session yourself"""
    save_shards(cfg=cfg, session=get_spark("imagenet-preprocessing"), iter_kwargs=asdict(cfg.iter_kwargs))


if __name__ == "__main__":
    main()
