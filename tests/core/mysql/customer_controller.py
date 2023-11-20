from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Customer

from core.logger import Logger
from core.db.mysql.transactional import mysql_transaction


logger = Logger().get_logger("mysql")


@mysql_transaction
async def get_all_customer(s: AsyncSession) -> list[Customer]:
    query = select(Customer)
    result = await s.execute(query)
    fetched_result = result.fetchall()
    return [row[0] for row in fetched_result]


@mysql_transaction
async def insert_customer(s: AsyncSession, args: dict):
    await s.execute(insert(Customer), args)
