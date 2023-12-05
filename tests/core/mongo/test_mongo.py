import pytest
import traceback
import datetime

from core.config import AppConfig
from core.logger import Logger
from core.db.mongo.session import connect_to_mongo


@pytest.mark.mongo
def test_mongo():
    # init config
    config = AppConfig().load_config("./test-config.toml")

    # logger init
    Logger().load_config(config)
    logger = Logger().get_logger("mongo")

    # connect to mongo
    try:
        client = connect_to_mongo()
    except BaseException as e:
        logger.error(traceback.format_exc())
        raise e

    db = client.test_db

    # insert
    post = {
        "author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }

    posts = db.posts
    _post_id = posts.insert_one(post).inserted_id

    first_post = posts.find_one()

    # delete
    posts.delete_many({})

    assert first_post is not None
