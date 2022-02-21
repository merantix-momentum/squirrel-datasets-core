from squirrel_datasets_core.datasets.kaggle_casting_quality.driver import RawKaggleCastingQualityDriver
from squirrel_datasets_core.parse_dataset_cards import parse_readme

__all__ = ["RawKaggleCastingQualityDriver", "DRIVERS", "DATASET_ATTRIBUTES"]
DRIVERS = [RawKaggleCastingQualityDriver]
DATASET_ATTRIBUTES = parse_readme(__name__)
