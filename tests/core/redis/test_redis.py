import pytest

from core.config import AppConfig
from core.logger import Logger
from core.db.redis.session import get_redis, close_redis


@pytest.mark.asyncio
async def test_redis():
    # load config
    config = AppConfig().load_config("./test-config.toml")

    # logger init
    Logger().load_config(config)

    redis = get_redis()
    try:
        await redis.set("chris", "happyguy")
        value = await redis.get("chris")
        assert b"happyguy" == value
    finally:
        await close_redis(redis)
