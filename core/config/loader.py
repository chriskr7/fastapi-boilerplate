import tomllib
from typing import Any

from core.patterns import Singleton


class AppConfig(metaclass=Singleton):
    def __init__(self):
        self._config = None

    def load_config(self, file_path: str) -> dict[str, Any] | None:
        with open(file_path, "rb") as file:
            self._config = tomllib.load(file)
        return self._config

    def get_config(self) -> dict[str, Any] | None:
        if self._config is not None:
            return self._config
        else:
            raise RuntimeError("Config is not initialized!")
