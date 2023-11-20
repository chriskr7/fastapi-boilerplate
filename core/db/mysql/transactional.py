import traceback
import functools

from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import Logger


logger = Logger().get_logger("mysql")


def mysql_transaction(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        if not isinstance(args[0], AsyncSession):
            raise AttributeError("First Argument MUST BE AsyncSession")
        session = args[0]
        try:
            result = await func(*args, **kwargs)
            await session.commit()
        except Exception as e:
            logger.error(traceback.format_exc())
            await session.rollback()
            raise e
        return result

    return wrapped
