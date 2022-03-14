from squirrel_datasets_core.datasets.imagenet.driver import RawImageNetDriver
from squirrel_datasets_core.parse_dataset_cards import parse_readme

__all__ = ["RawImageNetDriver", "DRIVERS", "DATASET_ATTRIBUTES"]
DRIVERS = [RawImageNetDriver]
DATASET_ATTRIBUTES = parse_readme(__name__)
