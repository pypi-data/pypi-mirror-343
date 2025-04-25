import pandas as pd
from _typeshed import Incomplete
from gllm_datastore.sql_data_store.adapter.sqlalchemy_adapter import SQLAlchemyAdapter as SQLAlchemyAdapter
from gllm_datastore.sql_data_store.constants import CREATE_ERROR_MSG as CREATE_ERROR_MSG, DELETE_ERROR_MSG as DELETE_ERROR_MSG, QUERY_ERROR_MSG as QUERY_ERROR_MSG, READ_ERROR_MSG as READ_ERROR_MSG, UNEXPECTED_ERROR_MSG as UNEXPECTED_ERROR_MSG, UPDATE_ERROR_MSG as UPDATE_ERROR_MSG
from gllm_datastore.sql_data_store.sql_data_store import BaseSQLDataStore as BaseSQLDataStore
from gllm_datastore.sql_data_store.types import QueryFilter as QueryFilter, QueryOptions as QueryOptions
from sqlalchemy import Engine as Engine
from sqlalchemy.orm import DeclarativeBase as DeclarativeBase
from typing import Any

class SQLAlchemySQLDataStore(BaseSQLDataStore):
    """Data store for interacting with SQLAlchemy.

    This class provides methods to interact with a SQL database using SQLAlchemy.

    Attributes:
        db (Engine): The SQLAlchemy engine object.
        logger (Logger): The logger object.
    """
    db: Incomplete
    logger: Incomplete
    def __init__(self, engine_or_url: Engine | str, pool_size: int = 50, max_overflow: int = 50, autoflush: bool = True) -> None:
        """Initialize SQLAlchemySQLDataStore class.

        Args:
            engine_or_url (Engine | str): SQLAlchemy engine object or database URL.
            pool_size (int, optional): The size of the database connections to be maintained. Defaults to 50.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 50.
            autoflush (bool, optional): If True, all changes to the database are flushed immediately. Defaults to True.

        Raises:
            ValueError: If the database adapter is not initialized.
        """
    async def query(self, query: str, params: dict[str, Any] | None = None) -> pd.DataFrame:
        '''Executes raw SQL queries.

        Preferred for complex queries, when working with legacy schemas without ORM models,
        or when using an LLM to generate your SQL queries.
        Use this method when you need advanced SQL operations not supported by read().

        Args:
            query (str): The query string with optional :param style parameters.
            params (dict[str, Any] | None, optional): Parameters to bind to the query. Defaults to None.

        Returns:
            pd.DataFrame: The result of the query.

        Note:
            Using string parameters directly in queries is unsafe and vulnerable to SQL injection.
            Therefore, please avoid doing as follows as they\'re unsafe:
            ```
            name = "O\'Connor"
            query = f"SELECT * FROM users WHERE last_name = \'{name}\'"
            ```
            or
            ```
            query = "SELECT * FROM users WHERE last_name = \'" + name + "\'"
            ```
            Instead, please use parameterized queries with :param style notation as follows:
            ```
            query = "SELECT * FROM users WHERE last_name = :last_name"
            params = {"last_name": "O\'Connor"}
            ```

        Raises:
            RuntimeError: If the query fails.
            RuntimeError: If an unexpected error occurs.
        '''
    def create(self, model: DeclarativeBase | list[DeclarativeBase]) -> None:
        '''Inserts data into the database using SQLAlchemy ORM.

        This method provides a structured way to insert data using ORM models.

        Args:
            model (DeclarativeBase | list[DeclarativeBase]): An instance or list of instances of SQLAlchemy
                model to be inserted.

        Example:
            To insert a row into a table:
            ```
            data_store.create(MyModel(column1="value1", column2="value2"))
            ```

            To insert multiple rows:
            ```
            data_store.create([
                MyModel(column1="value1", column2="value2"),
                MyModel(column1="value3", column2="value4")
            ])
            ```

        Raises:
            RuntimeError: If the insertion fails.
            RuntimeError: If an unexpected error occurs.
        '''
    def read(self, model_class: type[DeclarativeBase], filters: QueryFilter | None = None, options: QueryOptions | None = None) -> pd.DataFrame:
        '''Reads data from the database using SQLAlchemy ORM with a structured, type-safe interface.

        This method provides a high-level interface for querying data using ORM models. It supports
        filtering, column selection, ordering, and limiting results through a type-safe interface.

        Args:
            model_class (Type[DeclarativeBase]): The SQLAlchemy model class to query.
            filters (QueryFilter | None, optional): Optional query filters containing column-value pairs
                to filter the results. Defaults to None.
            options (QueryOptions | None, optional): Optional query configuration including:
                - columns: Specific columns to select
                - order_by: Column to sort by
                - order_desc: Sort order (ascending/descending)
                - limit: Maximum number of results
                Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the query results.

        Example:
            ```python
            data_store.read(
                Message,
                filters=QueryFilter(conditions={"conversation_id": "123"}),
                options=QueryOptions(
                    columns=["role", "content"],
                    order_by="created_at",
                    order_desc=True,
                    limit=10
                )
            )
            ```

        Raises:
            RuntimeError: If the read operation fails.
            RuntimeError: If an unexpected error occurs.
        '''
    def update(self, model_class: type[DeclarativeBase], update_values: dict[str, Any], filters: QueryFilter | None = None, **kwargs: Any) -> None:
        '''Updates data in the database using SQLAlchemy ORM.

        This method provides a structured way to update data using ORM models.

        Args:
            model_class (Type[DeclarativeBase]): The SQLAlchemy model class to update.
            update_values (dict[str, Any]): Values to update.
            filters (QueryFilter | None, optional): Filters to apply to the query. Defaults to None.
            **kwargs (Any): Additional keyword arguments to support the update method.

        Example:
            To update a row in a table:
            ```
            data_store.update(
                MyModel,
                update_values={"column1": "new_value"}
                filters=QueryFilter(conditions={"id": 1}),
            )
            ```

        Raises:
            RuntimeError: If the update operation fails.
            RuntimeError: If an unexpected error occurs.
        '''
    def delete(self, model_class: type[DeclarativeBase], filters: QueryFilter | None = None, allow_delete_all: bool = False, **kwargs: Any) -> None:
        '''Deletes data from the database using SQLAlchemy ORM.

        This method provides a structured way to delete data using ORM models.

        Args:
            model_class (Type[DeclarativeBase]): The SQLAlchemy model class to delete.
            filters (QueryFilter | None, optional): Filters to apply to the query. Defaults to None.
            allow_delete_all (bool, optional): If True, allows deletion of all records. Defaults to False.
            **kwargs (Any): Additional keyword arguments to support the delete method.

        Example:
            To delete a row from a table:
            ```
            data_store.delete(
                MyModel,
                filters=QueryFilter(conditions={"id": 1})
            )
            ```

        Raises:
            ValueError: If no filters are provided (to prevent accidental deletion of all records).
            RuntimeError: If the delete operation fails.
            RuntimeError: If an unexpected error occurs.
        '''
