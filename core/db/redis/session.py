import redis.asyncio as redis

from core.config import AppConfig


def get_redis(db: int = 0):
    app_cfg = AppConfig().get_config()
    if app_cfg is None:
        raise ModuleNotFoundError("config file is not initialized")
    redis_cfg = app_cfg["database"]["redis"]
    if db != 0:
        redis_cfg["db"] = db
    return redis.Redis(**redis_cfg)


async def close_redis(r: redis.Redis):
    await r.aclose()


async def yield_redis(db: int = 0):
    app_cfg = AppConfig().get_config()
    if app_cfg is None:
        raise ModuleNotFoundError("config file is not initialized")
    redis_cfg = app_cfg["database"]["redis"]
    if db != 0:
        redis_cfg["db"] = db
    r = redis.Redis(**redis_cfg)
    yield r
    await r.aclose()
