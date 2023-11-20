from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from core.config import AppConfig

engine = None
async_session = None


class Base(DeclarativeBase, MappedAsDataclass):
    pass


def init_db_engine() -> AsyncEngine:
    config_ = AppConfig().get_config()
    if config_ is None:
        raise ModuleNotFoundError("config file is not initialized")
    mysql_cfg = config_["database"]["mysql"]
    DB_URL = (
        "mysql+aiomysql://{0}:{1}@{2}:{3}/{4}?charset=UTF8MB4&use_unicode=1".format(
            mysql_cfg["user"],
            mysql_cfg["password"],
            mysql_cfg["host"],
            mysql_cfg["port"],
            mysql_cfg["db_name"],
        )
    )

    global engine
    engine = create_async_engine(
        DB_URL,
        future=True,
        echo=mysql_cfg["echo"] if "echo" in mysql_cfg else False,
        pool_size=mysql_cfg["pool_size"],
        pool_recycle=mysql_cfg["pool_recycle"],
    )

    global async_session
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return engine


async def get_session() -> AsyncSession:
    global async_session
    if async_session is None:
        raise ModuleNotFoundError("async_session is not initialized")
    async with async_session() as session:
        return session


async def yield_session() -> AsyncIterator[AsyncSession]:
    global async_session
    if async_session is None:
        raise ModuleNotFoundError("async_session is not initialized")
    async with async_session() as session:
        yield session


async def dispose_engine():
    global engine
    if engine is not None:
        await engine.dispose()
