import logging
from collections.abc import Iterable

from duckdb import (
    ColumnExpression,
    DuckDBPyConnection,
    DuckDBPyRelation,
)

from mallardetl import LoadableContext, Processor
from mallardetl.error import LoadError

logger = logging.getLogger(__name__)


class Dimension(LoadableContext):
    def __init__(
        self,
        con: DuckDBPyConnection,
        src_tbl: str,
        dst_db: str,
        dst_tbl: str,
        key: str,
        join_keys: Iterable[str],
        name_map: dict[str, str],
        dst_schema: str | None = None,
        processor: Processor = Processor(),
        id_seq_start: int = 1,
    ) -> None:
        self.__con = con
        super().__init__(
            src_tbl=src_tbl,
            dst_db=dst_db,
            dst_tbl=dst_tbl,
            join_keys=join_keys,
            name_map=name_map,
            dst_schema=dst_schema,
        )

        self.__key = key
        self.__is_smart_key = key in join_keys
        self.__processor = processor
        self.__id_seq_start = id_seq_start
        self.__max_id = None

        self.__seq_name = f"{dst_tbl}_{key}_seq"

    @property
    def key(self) -> str:
        return self.__key

    @property
    def id_seq_start(self) -> int:
        return self.__id_seq_start

    @property
    def max_id(self) -> int:
        if self.__max_id is None:
            self.__max_id = self.__con.query(
                f"""
SELECT coalesce(greatest(max({self.__key}), $id_seq_start), $id_seq_start)
FROM {self.dst};""",
                params={"id_seq_start": self.__id_seq_start - 1},
            ).fetchall()[0][0]

        return self.__max_id

    def __validate(self):
        src_columns = self.__con.table(self.src_tbl).columns
        mapped_join_keys = {self.name_map[k] for k in self.join_keys}
        diff = mapped_join_keys.difference(src_columns)

        if len(diff) != 0:
            raise LoadError(f"Missing join keys in source table: {diff}")

    def __select_dim_columns(self, src: DuckDBPyRelation) -> DuckDBPyRelation:
        columns = [ColumnExpression(v).alias(k) for k, v in self.name_map.items()]
        return src.select(*columns)

    def __reduce(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        value_cols = set(self.name_map.keys()).difference(self.join_keys)
        expr = [f"last({c}) AS {c}" for c in value_cols]

        reduced_tbl = tbl.query(
            "all_values",
            f"""
SELECT {",".join(self.join_keys)},
       {",".join(expr)}
FROM all_values
GROUP BY {",".join(self.join_keys)};
""",
        )

        if len(tbl.distinct()) > len(reduced_tbl):
            logger.warning(
                "Conflicting attribute values for %s found in the source data having the same join_key %s."
                "Only the last attribute value from the source data are used in conflicting rows, i.e. intermediate values are not stored in the dimension table. "
                "Should this behavior not be desired, consider using a slowly changing dimension.",
                self.dst_tbl,
                self.join_keys,
            )

        return reduced_tbl

    def __join(self, tbl: DuckDBPyRelation) -> DuckDBPyRelation:
        dst = (  # noqa: F841
            self.__con.query(f"SELECT * FROM {self.dst}")
            .select(self.__key, *self.join_keys)
            .set_alias("dst")
        )

        join_conditions = [
            f"src.{k} IS NOT DISTINCT FROM dst.{k}" for k in self.join_keys
        ]
        join_expression = " AND ".join(join_conditions)

        q: str

        if self.__is_smart_key:
            q = f"""
SELECT coalesce(src.{self.__key}, dst.{self.__key}) AS {self.__key},
    (src.* EXCLUDE ({self.__key})),
    dst.{self.__key} IS NULL AS is_new
FROM tbl AS src
LEFT JOIN dst ON {join_expression};
"""
        else:
            q = f"""
SELECT dst.{self.__key},
    src.*, 
    dst.{self.__key} IS NULL AS is_new
FROM tbl AS src
LEFT JOIN dst ON {join_expression};
"""

        return self.__con.query(q)

    def __assign_missing_ids(self, tbl: DuckDBPyRelation):
        if self.__is_smart_key:
            return tbl

        self.__con.execute(
            f"CREATE TEMP SEQUENCE {self.__seq_name} START {self.max_id + 1};"
        )

        return self.__con.query(
            f"""
SELECT *
REPLACE (
    ifnull({self.__key}, nextval('{self.__seq_name}')) AS {self.__key}
)
FROM tbl;
"""
        )

    def __load_new_values(self, tbl: DuckDBPyRelation):
        if self.__is_smart_key:
            columns = []
        else:
            columns = [self.__key]
        columns += list(self.name_map.keys())

        q = f"""
INSERT INTO {self.dst} ({", ".join(columns)}) 
FROM (
    SELECT {", ".join(columns)} 
    FROM tbl
    WHERE is_new
);"""
        self.__con.execute(q)

    def __update_src(self, tbl: DuckDBPyRelation):
        # Smart keys are precomputed, and therefore already exist in src
        if self.__is_smart_key:
            return

        key_col_type = tbl.select(self.__key).types[0]

        q = f"ALTER TABLE {self.src_tbl} ADD COLUMN IF NOT EXISTS {self.__key} {key_col_type};"
        self.__con.execute(q)

        join_conditions = [
            f"src.{self.name_map[c]} IS NOT DISTINCT FROM tbl.{c}"
            for c in self.join_keys
        ]
        join_expression = " AND ".join(join_conditions)

        q = f"""
UPDATE {self.src_tbl} AS src 
    SET {self.__key} = tbl.{self.__key}
    FROM tbl
    WHERE {join_expression};"""
        self.__con.execute(q)

    def load(self):
        self.__validate()
        src = self.__con.table(self.src_tbl)
        transformed_src = self.__processor.transform(src, self)
        tbl = self.__select_dim_columns(transformed_src)
        tbl = self.__reduce(tbl)
        tbl = self.__join(tbl)
        tbl = self.__assign_missing_ids(tbl)

        logger.info(
            "Inserting %s new rows into %s",
            format(len(tbl.filter("is_new")), ","),
            self.dst_tbl,
        )

        tbl.to_table(self.dst_tbl)
        tbl = self.__con.table(self.dst_tbl)

        self.__processor.pre_load(tbl, self)
        self.__load_new_values(tbl)
        self.__processor.post_load(tbl, self)

        self.__update_src(tbl)

        self.__con.execute(f"DROP TABLE {self.dst_tbl};")
