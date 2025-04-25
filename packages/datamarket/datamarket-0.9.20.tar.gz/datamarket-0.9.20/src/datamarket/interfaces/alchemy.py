########################################################################################################################
# IMPORTS

import logging
from collections.abc import MutableMapping
from typing import Any, Iterator, List, Type, TypeVar
from urllib.parse import quote_plus

from sqlalchemy import DDL, FrozenResult, Result, Select, SQLColumnExpression, create_engine, func, select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

########################################################################################################################
# CLASSES

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class MockContext:
    def __init__(self, column: SQLColumnExpression) -> None:
        self.current_parameters = {}
        self.current_column = column
        self.connection = None


class AlchemyInterface:
    def __init__(self, config: MutableMapping) -> None:
        if "db" in config:
            self.config = config["db"]

            self.engine = create_engine(self.get_conn_str())
            self.session = sessionmaker(bind=self.engine)()
            self.cursor = self.session.connection().connection.cursor()

        else:
            logger.warning("no db section in config")

    def get_conn_str(self):
        return (
            f"{self.config['engine']}://"
            f"{self.config['user']}:{quote_plus(self.config['password'])}"
            f"@{self.config['host']}:{self.config['port']}"
            f"/{self.config['database']}"
        )

    @staticmethod
    def get_schema_from_table(table: Type[ModelType]) -> str:
        schema = "public"

        if isinstance(table.__table_args__, tuple):
            for table_arg in table.__table_args__:
                if isinstance(table_arg, dict) and "schema" in table_arg:
                    schema = table_arg["schema"]

        elif isinstance(table.__table_args__, dict) and "schema" in table.__table_args__:
            schema = table.__table_args__["schema"]

        if schema == "public":
            logger.warning(f"no database schema provided, switching to {schema}...")

        return schema

    def create_tables(self, tables: List[Type[ModelType]]) -> None:
        for table in tables:
            schema = self.get_schema_from_table(table)

            with self.engine.connect() as conn:
                conn.execute(DDL(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                conn.commit()

                if hasattr(table, "is_view") and table.is_view:
                    if not conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"creating view {table.__tablename__}...")
                        table.create_view(conn)
                        conn.commit()
                    else:
                        logger.info(f"view {table.__tablename__} already exists")
                else:
                    if not conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"creating table {table.__tablename__}...")
                        table.__table__.create(conn)
                        conn.commit()
                    else:
                        logger.info(f"table {table.__tablename__} already exists")

    def drop_tables(self, tables: List[Type[ModelType]]) -> None:
        for table in tables:
            schema = self.get_schema_from_table(table)

            with self.engine.connect() as conn:
                if hasattr(table, "is_view") and table.is_view:
                    if conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"dropping view {table.__tablename__}...")
                        conn.execute(DDL(f"DROP VIEW {schema}.{table.__tablename__} CASCADE"))
                        conn.commit()
                else:
                    if conn.dialect.has_table(conn, table.__tablename__, schema=schema):
                        logger.info(f"dropping table {table.__tablename__}...")
                        conn.execute(DDL(f"DROP TABLE {schema}.{table.__tablename__} CASCADE"))
                        conn.commit()

    def reset_db(self, tables: List[Type[ModelType]], drop: bool = False) -> None:
        if drop:
            self.drop_tables(tables)

        self.create_tables(tables)

    def reset_column(self, query_results: List[Result[Any]], column_name: str) -> None:
        if not query_results:
            logger.warning("No objects to reset column for.")
            return

        first_obj = query_results[0]
        model_class = first_obj.__class__
        table = model_class.__table__

        if column_name not in table.columns:
            logger.warning(f"Column {column_name} does not exist in table {table.name}.")
            return

        column = table.columns[column_name]

        if column.server_default is not None:
            query_results.update({column_name: text("DEFAULT")}, synchronize_session=False)
        elif column.default is not None:
            default_value = column.default.arg
            if callable(default_value):
                default_value = default_value(MockContext(column))
            query_results.update({column_name: default_value}, synchronize_session=False)
        else:
            raise ValueError(f"Column '{column_name}' doesn't have a default value defined.")

        self.session.commit()

    def insert_alchemy_obj(self, alchemy_obj: ModelType, silent: bool = False) -> None:
        try:
            if not silent:
                logger.info(f"adding {alchemy_obj}...")

            self.session.add(alchemy_obj)
            self.session.commit()

        except IntegrityError:
            if not silent:
                logger.info(f"{alchemy_obj} already in db")

            self.session.rollback()

    def upsert_alchemy_obj(self, alchemy_obj: ModelType, index_elements: List[str], silent: bool = False) -> None:
        if not silent:
            logger.info(f"upserting {alchemy_obj}")

        primary_keys = list(col.name for col in alchemy_obj.__table__.primary_key.columns.values())
        obj_dict = {
            col.name: val
            for col in alchemy_obj.__table__.columns
            if col.name not in primary_keys and (val := getattr(alchemy_obj, col.name)) is not None
        }

        statement = (
            insert(alchemy_obj.__table__)
            .values(obj_dict)
            .on_conflict_do_update(index_elements=index_elements, set_=obj_dict)
        )

        try:
            self.session.execute(statement)
            self.session.commit()
        except IntegrityError:
            if not silent:
                logger.info(f"could not upsert {alchemy_obj}")

            self.session.rollback()

    def windowed_query(
        self,
        stmt: Select[Any],
        order_by: List[SQLColumnExpression[Any]],
        windowsize: int,
    ) -> Iterator[Result[Any]]:
        """
        Executes a windowed query on the given statement.

        Args:
            stmt: The SQL select statement to execute.
            order_by: The columns to use for ordering.
            windowsize: The number of rows to fetch in each window.

        Returns:
            An iterator of Result objects, each containing a window of data.

        More info: https://github.com/sqlalchemy/sqlalchemy/wiki/RangeQuery-and-WindowedRangeQuery
        """
        # Add row_number over the specified order
        row_number = func.row_number().over(order_by=order_by).label("row_number")

        # Add the windowing column to the statement and sort by it for deterministic results
        inner_stmt = stmt.add_columns(row_number).order_by(row_number)
        subq = inner_stmt.subquery()

        # Create an outer query that selects from the subquery
        cols = [c for c in subq.c]
        outer_query = select(*cols)

        last_row_number = 0

        while True:
            # Filter on row_number in the outer query
            current_query = outer_query.where(subq.c.row_number > last_row_number).limit(windowsize)
            result = self.session.execute(current_query)

            # Create a FrozenResult to allow peeking at the data without consuming
            frozen_result: FrozenResult = result.freeze()
            chunk = frozen_result().all()

            if not chunk:
                break

            # Update for next iteration
            last_row_number = chunk[-1].row_number - 1

            # Create a new Result object from the FrozenResult
            yield_result = frozen_result()

            # Remove row_number from result
            yield_result = yield_result.columns(*range(len(cols) - 1))

            yield yield_result
