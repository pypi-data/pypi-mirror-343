import logging
from collections.abc import Iterable

from duckdb import ColumnExpression, DuckDBPyConnection, DuckDBPyRelation

from mallardetl import LoadableContext, Processor

logger = logging.getLogger(__name__)


class Fact(LoadableContext):
    def __init__(
        self,
        con: DuckDBPyConnection,
        src_tbl: str,
        dst_db: str,
        dst_tbl: str,
        join_keys: Iterable[str],
        name_map: dict[str, str],
        dst_schema: str | None = None,
        processor: Processor = Processor(),
    ) -> None:
        super().__init__(
            src_tbl, dst_db, dst_tbl, join_keys, name_map, dst_schema=dst_schema
        )
        self.__con = con
        self.__processor = processor
        self.__loaded_rows = 0

    @property
    def loaded_rows(self) -> int:
        """
        The number of rows that have been loaded from the source into the fact table.

        The value is set after the `load` method has been called. It is reset to 0
        each time the `load` method is called.
        """
        return self.__loaded_rows

    def __select_dim_columns(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        columns = [ColumnExpression(v).alias(k) for k, v in self.name_map.items()]
        return tbl.select(*columns)

    def __load_values(self, tbl: DuckDBPyRelation):
        columns = list(self.name_map.keys())
        logger.info("Loading source data into %s", self.dst_tbl)
        q = f"INSERT INTO {self.dst} ({', '.join(columns)}) FROM (SELECT {', '.join(columns)} FROM tbl);"
        self.__con.execute(q)

    def load(self) -> None:
        self.__loaded_rows = 0
        src = self.__con.table(self.src_tbl)

        logger.debug("Transforming source data")
        transformed_src = self.__processor.transform(src, self)

        logger.debug("Selecting fact table columns, %s", list(self.name_map.keys()))
        tbl = self.__select_dim_columns(transformed_src)

        logger.debug("Applying pre-load")
        tbl = self.__processor.pre_load(tbl, self)
        self.__load_values(tbl)
        self.__loaded_rows = len(tbl)

        logger.debug("Applying post-load")
        self.__processor.post_load(tbl, self)
        logger.info("Loaded %s rows into %s", f"{self.loaded_rows:,}", self.dst)
