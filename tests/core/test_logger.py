import os
import pytest
from core.config import AppConfig
from core.logger import Logger


@pytest.mark.logger
def test_logger():
    # loading config file
    file_path = "./test-config.toml"
    config = AppConfig().load_config(file_path)

    # init logger
    Logger().load_config(config)
    general_logger = Logger().get_logger("general")

    general_logger.info("logging test")

    target_file_path = "./logs/general.log"
    with open(target_file_path, "r") as file:
        test_str = file.read()
        assert "logging test" in test_str

    os.system("rm -rf ./logs")
