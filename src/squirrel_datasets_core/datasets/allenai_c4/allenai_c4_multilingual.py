from __future__ import annotations

import typing as t

import fsspec
from squirrel.driver import MapDriver
from squirrel.serialization import JsonSerializer

if t.TYPE_CHECKING:
    from squirrel.iterstream import Composable


class C4DatasetDriver(MapDriver):

    name = "c4"

    def __init__(
        self,
        subsets: t.Dict[str, t.Dict[str, t.List]],
        deser_hook: t.Optional[t.Callable] = None,
        compression: t.Optional[str] = "gzip",
        **kwargs,
    ) -> None:
        """Initialize the driver.

        Args:
            subsets: Map of iso language string to dict containing a map of split to list of all shard urls.
            deser_hook (Callable): Callable that is passed as `object_hook` to :py:class:`JsonDecoder` during json
                deserialization. Defaults to None.
            compression (str, optional): Compression codec to use. Passed to :py:func:`fsspec.open` when opening files
                to read. Defaults to "gzip".
            **kwargs: Other keyword arguments passed to super class initializer.
        """
        super().__init__(**kwargs)
        self._subsets = subsets
        self._lang = list(self._subsets.keys())
        self._split = "train"
        self._source = None

        self.deser_hook = deser_hook
        self.compression = compression

    def _init_source(self, lang: t.List[str], split: str) -> None:
        """
        Lazy initialization for the source generator.

        Args:
            lang: list of iso strings that the source should contain.
            split: denotes the train or valid split of C4.
        """
        self._source = []
        for iso in lang:
            self._source += self._subsets[iso][split]

    def select(self, lang: t.Optional[t.Union[str, t.List[str]]] = None, split: str = "train") -> C4DatasetDriver:
        """Select a specific subset and/or split of the C4 dataset.

        Args:
            lang: list of iso strings for the languages to be selected.
            split: denotes the train or valid split of C4.
        """
        if lang is not None:
            if isinstance(lang, str):
                lang = [lang]

            self._lang = lang

        self._split = split
        self._init_source(self._lang, self._split)
        return self

    @property
    def available_languages(self) -> t.List[str]:
        """Returns a list of all available languages in the C4 corpus."""
        return list(self._subsets.keys())

    def keys(self) -> t.List[str]:
        """Returns the list of urls for the archive files for the selected subset and/or split."""
        return self._source

    @staticmethod
    def get(url: str, compression: t.Optional[str] = "gzip") -> t.Iterator:
        """Yields samples from a C4 dataset archive file.

        Args:
            url (str): Path to the archive file.
            compression (str, optional): Compression codec to use. Passed to :py:func:`fsspec.open` when opening files
                to read. Defaults to "gzip".

        Yields:
            Samples from selected subset and/or splits.
        """
        ser = JsonSerializer()

        with fsspec.open(url, compression=compression, mode="r") as f:
            for line in f.readlines():
                yield ser.deserialize(line)

    def get_iter(self, **kwargs) -> Composable:
        """Returns an iterable of items in the form of a :py:class:`squirrel.iterstream.Composable`, which allows
        various stream manipulation functionalities. Only sets the compression method by default. For available keyword
        arguments, refer to :py:meth:`MapDriver.get_iter`.
        """
        return super().get_iter(flatten=True, get_kwargs={"compression": self.compression}, **kwargs)
