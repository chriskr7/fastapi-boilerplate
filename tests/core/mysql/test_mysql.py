import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppConfig
from core.logger import Logger
from core.db.mysql import session as mysql_manager


async def drop_customer_table(s: AsyncSession):
    query = text("DROP TABLE CUSTOMER")
    await s.execute(query)


async def create_customer_table(s: AsyncSession):
    query = text(
        """
        CREATE TABLE CUSTOMER (
            id  INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(20) NOT NULL,
            email VARCHAR(40) NOT NULL
        )"""
    )
    await s.execute(query)


@pytest.mark.asyncio
async def test_mysql():
    # load config
    config = AppConfig().load_config("./test-config.toml")

    # logger init
    Logger().load_config(config)

    # db init
    mysql_manager.init_db_engine()
    session = await mysql_manager.get_session()

    # drop table
    await drop_customer_table(session)

    # create table
    await create_customer_table(session)

    from .customer_controller import insert_customer, get_all_customer

    insert_args = {
        "name": "chris",
        "email": "chriskr7@gmail.com",
    }
    await insert_customer(session, insert_args)

    rslt_list = await get_all_customer(session)
    customer = rslt_list[0]

    try:
        assert "chris" == customer.name
        assert "chriskr7@gmail.com" == customer.email
    finally:
        await session.close()
        await mysql_manager.dispose_engine()
