import pytest
from core.config import AppConfig


@pytest.mark.config_test
def test_config():
    file_path = "./test-config.toml"
    config = AppConfig().load_config(file_path)

    assert config is not None
    config_dict = {
        "logger": {
            "access": {"level": "debug", "path": "./logs", "filename": "access.log"},
            "application": {
                "level": "debug",
                "path": "./logs",
                "filename": "application.log",
            },
            "general": {"level": "debug", "path": "./logs", "filename": "general.log"},
            "mysql": {"level": "debug", "path": "./logs", "filename": "mysql.log"},
        },
        "database": {
            "mysql": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "root",
                "db_name": "test",
                "pool_size": 10,
                "pool_recycle": 1024,
                "echo": True,
            }
        },
    }

    if config is not None:
        assert config == config_dict
