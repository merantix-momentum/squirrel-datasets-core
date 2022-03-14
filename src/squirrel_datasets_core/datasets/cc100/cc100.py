from __future__ import annotations

import typing as t

import fsspec
from squirrel.driver import MapDriver
from squirrel.iterstream import Composable
from squirrel.iterstream.source import IterableSource

if t.TYPE_CHECKING:
    from squirrel.catalog import Catalog


class CC100Driver(MapDriver):

    name = "cc100"

    def __init__(
        self, subsets: t.Dict[str, str], catalog: t.Optional[Catalog] = None, compression: str = "xz", **kwargs
    ):
        """
        Initialize the store
        Args:
            subsets: a mapping of iso language string to the corresponding url where the data is found
            catalog: a `squirrel.catalog.Catalog` that contains configuration for custom dataset locations.
            compression: the default compression for the files. Defaults to `xz`.
        """
        super().__init__(catalog=catalog, **kwargs)
        self._subsets = subsets
        self._lang = list(self._subsets.keys())
        self._source = None

        self.compression = compression

    @property
    def _file_path_generator(self) -> IterableSource:
        """Initializes the source for the CC100Driver to iterate over."""
        if self._source is None:
            self._init_source(self._lang)

        return IterableSource(self._source)

    def _init_source(self, lang: t.List[str]) -> None:
        """
        Lazy initialization for the source generator.

        Args:
            lang: list of iso strings that the source should contain.
        """
        self._source = [self._subsets[iso] for iso in lang]

    def select(self, lang: t.Optional[t.Union[str, t.List[str]]] = None) -> CC100Driver:
        """
        Select a specific subset and/or split of the c4 dataset.

        Args:
            lang: list of iso strings for the languages to be selected.
        """
        if lang is not None:
            if isinstance(lang, str):
                lang = [lang]

            self._lang = lang

        return self

    def keys(self, **kwargs) -> t.List[str]:
        """Returns the list of urls for the archive file of the selected language(s)."""
        if self._source is None:
            self._init_source(self._lang)

        return self._source

    @staticmethod
    def get(url: str, compression: t.Optional[str] = None) -> t.List:
        """
        Read a single record in the CC100 dataset. Takes into account the special formatting of the data.

        Args:
            url: str that points to the web-location of the dataset shard
            compression: specifies the compression algorithm of the dataset.
        """
        with fsspec.open(url, "rb", compression=compression) as fp:
            text = "".join([line.decode("utf-8") for line in fp.readlines()])

        return [{"text": elem} for elem in text.split("\n\n")]

    def get_iter(self, **kwargs) -> Composable:
        """Returns an iterable of items in the form of a :py:class:`squirrel.iterstream.Composable`, which allows
        various stream manipulation functionalities. Only sets the compression method by default. For available keyword
        arguments, refer to :py:meth:`MapDriver.get_iter`.
        """
        return super().get_iter(flatten=True, get_kwargs={"compression": self.compression}, **kwargs)

    @property
    def available_languages(self) -> t.List[str]:
        """Returns a list of all available languages in the C4 corpus."""
        return list(self._subsets.keys())
