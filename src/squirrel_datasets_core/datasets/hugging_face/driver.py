from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from datasets import load_dataset
from squirrel.driver import RecordIteratorDriver
from squirrel.iterstream import IterableSource

if TYPE_CHECKING:
    from squirrel.catalog.catalog import Catalog
    from squirrel.iterstream import Composable


class HuggingfaceDriver(RecordIteratorDriver):
    name = "huggingface"

    def __init__(
        self, name: str, subset: str = None, streaming: bool = True, catalog: Optional[Catalog] = None, **kwargs
    ) -> None:
        """Load huggingface dataset"""
        super().__init__(catalog=catalog)
        self._dataset = load_dataset(path=name, name=subset, streaming=streaming, **kwargs)

    def get_iter(self, split: str, **kwargs) -> Composable:
        """Create iterstream based on dataset split."""
        return IterableSource(self._dataset[split])

    def get_store(self, **kwargs) -> Any:
        """Get the huggingface dataset object"""
        return self._dataset
