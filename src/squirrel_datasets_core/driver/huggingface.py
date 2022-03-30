from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import datasets
from datasets import load_dataset
from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource

if TYPE_CHECKING:
    from squirrel.catalog.catalog import Catalog

# Disable TQDM bars
datasets.logging.set_verbosity(datasets.logging.WARNING)


class HuggingfaceDriver(IterDriver):
    name = "huggingface"

    def __init__(
        self,
        name: str,
        subset: Optional[str] = None,
        streaming: bool = True,
        catalog: Optional[Catalog] = None,
        **kwargs,
    ) -> None:
        """Load huggingface dataset."""
        super().__init__(catalog=catalog)
        self._dataset = load_dataset(path=name, name=subset, streaming=streaming, **kwargs)

    def get_iter(self, split: str) -> IterableSource:
        """Create iterstream based on dataset split."""
        return IterableSource(self._dataset[split])
