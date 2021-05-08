import sys
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import TypeVar

from .row import Row as Row
from ..sql.base import InPlaceGenerative
from ..util import collections_abc

_TResult = TypeVar("_TResult", bound=Result)
_TScalarResult = TypeVar("_TScalarResult", bound=ScalarResult)
_TMappingResult = TypeVar("_TMappingResult", bound=MappingResult)
_TChunkedIteratorResult = TypeVar(
    "_TChunkedIteratorResult", bound=ChunkedIteratorResult
)

def tuplegetter(*indexes: Any) -> Callable[[Any], Tuple[Any, ...]]: ...

class ResultMetaData:
    @property
    def keys(self) -> RMKeyView: ...

class RMKeyView(collections_abc.KeysView[str]):
    def __init__(self, parent: Any) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[str]: ...
    def __contains__(self, item: object) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...

class SimpleResultMetaData(ResultMetaData):
    def __init__(
        self,
        keys: Iterable[str],
        extra: Optional[Any] = ...,
        _processors: Optional[Any] = ...,
        _tuplefilter: Optional[Any] = ...,
        _translated_indexes: Optional[Any] = ...,
        _unique_filters: Optional[Any] = ...,
    ) -> None: ...

def result_tuple(fields: Any, extra: Optional[Any] = ...) -> Row: ...

class ResultInternal(InPlaceGenerative): ...

class _WithKeys:
    def keys(self) -> RMKeyView: ...

class Result(_WithKeys, ResultInternal):
    def __init__(self, cursor_metadata: ResultMetaData) -> None: ...
    def yield_per(self: _TResult, num: Any) -> _TResult: ...
    def unique(
        self: _TResult, strategy: Optional[object] = ...
    ) -> _TResult: ...
    def columns(self: _TResult, *col_expressions: object) -> _TResult: ...
    def scalars(self, index: int = ...) -> ScalarResult: ...
    def mappings(self) -> MappingResult: ...
    def __iter__(self) -> Iterator[Row]: ...
    def __next__(self) -> Row: ...
    if sys.version_info < (3, 0):
        def next(self) -> Row: ...
    def partitions(self, size: Optional[int] = ...) -> Iterator[List[Row]]: ...
    def fetchall(self) -> List[Row]: ...
    def fetchone(self) -> Optional[Row]: ...
    def fetchmany(self, size: Optional[int] = ...) -> List[Row]: ...
    def all(self) -> List[Row]: ...
    def first(self) -> Optional[Row]: ...
    def one_or_none(self) -> Optional[Row]: ...
    def scalar_one(self) -> Any: ...
    def scalar_one_or_none(self) -> Optional[Any]: ...
    def one(self) -> Row: ...
    def scalar(self) -> Optional[Any]: ...
    def freeze(self) -> FrozenResult: ...
    def merge(self, *others: Result) -> MergedResult: ...

class FilterResult(ResultInternal): ...

class ScalarResult(FilterResult):
    def __init__(self, real_result: Result, index: Any) -> None: ...
    def unique(
        self: _TScalarResult, strategy: Optional[Any] = ...
    ) -> _TScalarResult: ...
    def partitions(self, size: Optional[int] = ...) -> Iterator[List[Any]]: ...
    def fetchall(self) -> List[Any]: ...
    def fetchmany(self, size: Optional[int] = ...) -> List[Any]: ...
    def all(self) -> List[Any]: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __next__(self) -> Any: ...
    if sys.version_info < (3, 0):
        def next(self) -> Any: ...
    def first(self) -> Optional[Any]: ...
    def one_or_none(self) -> Optional[Any]: ...
    def one(self) -> Any: ...

class MappingResult(_WithKeys, FilterResult):
    def __init__(self, result: Result) -> None: ...
    def unique(
        self: _TMappingResult, strategy: Optional[Any] = ...
    ) -> _TMappingResult: ...
    def columns(
        self: _TMappingResult, *col_expressions: object
    ) -> _TMappingResult: ...
    def partitions(
        self, size: Optional[int] = ...
    ) -> Iterator[List[Mapping[Any, Any]]]: ...
    def fetchall(self) -> List[Mapping[Any, Any]]: ...
    def fetchone(self) -> Mapping[Any, Any]: ...
    def fetchmany(
        self, size: Optional[int] = ...
    ) -> List[Mapping[Any, Any]]: ...
    def all(self) -> List[Mapping[Any, Any]]: ...
    def __iter__(self) -> Iterator[Mapping[Any, Any]]: ...
    def __next__(self) -> Mapping[Any, Any]: ...
    if sys.version_info < (3, 0):
        def next(self) -> Mapping[Any, Any]: ...
    def first(self) -> Optional[Mapping[Any, Any]]: ...
    def one_or_none(self) -> Optional[Mapping[Any, Any]]: ...
    def one(self) -> Mapping[Any, Any]: ...

class FrozenResult:
    metadata: Any = ...
    data: Any = ...
    def __init__(self, result: Result) -> None: ...
    def rewrite_rows(self) -> List[List[Any]]: ...
    def with_new_rows(
        self, tuple_data: List[Tuple[Any, ...]]
    ) -> FrozenResult: ...
    def __call__(self) -> IteratorResult: ...

class IteratorResult(Result):
    iterator: Any = ...
    raw: Any = ...
    def __init__(
        self,
        cursor_metadata: ResultMetaData,
        iterator: Any,
        raw: Optional[Any] = ...,
    ) -> None: ...

def null_result() -> IteratorResult: ...

class ChunkedIteratorResult(IteratorResult):
    chunks: Any = ...
    raw: Any = ...
    iterator: Any = ...
    dynamic_yield_per: Any = ...
    def __init__(
        self,
        cursor_metadata: ResultMetaData,
        chunks: Any,
        source_supports_scalars: bool = ...,
        raw: Optional[Any] = ...,
        dynamic_yield_per: bool = ...,
    ) -> None: ...
    def yield_per(
        self: _TChunkedIteratorResult, num: Any
    ) -> _TChunkedIteratorResult: ...

class MergedResult(IteratorResult):
    closed: bool = ...
    def __init__(
        self, cursor_metadata: ResultMetaData, results: Result
    ) -> None: ...
    def close(self) -> None: ...
