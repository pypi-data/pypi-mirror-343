from abc import ABC
from collections.abc import Iterable

from duckdb import DuckDBPyRelation


class LoadableContext(ABC):
    def __init__(
        self,
        src_tbl: str,
        dst_db: str,
        dst_tbl: str,
        join_keys: Iterable[str],
        name_map: dict[str, str],
        dst_schema: str | None = None,
    ) -> None:
        self._src_tbl = src_tbl
        self._dst_db = dst_db
        self._dst_schema = dst_schema
        self._dst_tbl = dst_tbl
        self._join_keys = join_keys
        self._name_map = name_map

    @property
    def src_tbl(self) -> str:
        return self._src_tbl

    @property
    def dst_db(self) -> str:
        return self._dst_db

    @property
    def dst_schema(self) -> str | None:
        return self._dst_schema

    @property
    def dst_tbl(self) -> str:
        return self._dst_tbl

    @property
    def dst(self) -> str:
        dst = f'"{self._dst_db}"'

        if self._dst_schema:
            dst += f'."{self._dst_schema}"'

        return dst + f'."{self._dst_tbl}"'

    @property
    def join_keys(self) -> Iterable[str]:
        return self._join_keys

    @property
    def name_map(self) -> dict[str, str]:
        return self._name_map


class Processor(ABC):
    def transform(
        self, tbl: DuckDBPyRelation, ctx: LoadableContext
    ) -> DuckDBPyRelation:
        return tbl

    def pre_load(self, tbl: DuckDBPyRelation, ctx: LoadableContext) -> DuckDBPyRelation:
        return tbl

    def post_load(self, tbl: DuckDBPyRelation, ctx: LoadableContext) -> None: ...
