from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from core.config import AppConfig


def connect_to_mongo() -> MongoClient:
    config_ = AppConfig().get_config()
    if config_ is None:
        raise ModuleNotFoundError("config file is not initialized")
    mongo_cfg = config_["database"]["mongo"]

    try:
        client = MongoClient(
            host=mongo_cfg["host"],
            port=mongo_cfg["port"],
            username=mongo_cfg["user"],
            password=mongo_cfg["password"],
            authSource=mongo_cfg["auth_source"],
            authMechanism=mongo_cfg["auth_mechanism"],
        )
    except ConnectionFailure as e:
        raise e
    return client
