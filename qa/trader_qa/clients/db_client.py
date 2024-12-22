# pylint: disable=no-value-for-parameter
import allure
from sqlalchemy import MetaData, Table, create_engine, delete, func, select
from sqlalchemy.orm import Session

from trader_qa.constants import Table as TableName


class DBClient:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url)
        self._metadata = MetaData(bind=self._engine)
        self._session = Session(bind=self._engine, autoflush=True, autocommit=True)

        self._order_table = Table(TableName.ORDERS.value, self._metadata, autoload_with=self._engine)

    @allure.step
    def delete_order(self, order_id: int) -> None:
        query = self._order_table.delete().where(self._order_table.c.id == order_id)

        with self._engine.connect() as conn:
            conn.execute(query)

    def check_db_isolation(self) -> dict[str, int]:
        affected_tables = {}

        for table_name in TableName:
            table = Table(table_name.value, self._metadata, autoload_with=self._engine)
            query = select([func.count()]).select_from(table)

            with self._engine.connect() as conn:
                count = conn.execute(query).scalar()

                if count != 0:
                    affected_tables[table.name] = count
                    conn.execute(delete(table))

        return affected_tables
