import configparser

from typing import Optional


class ConfigParser(configparser.ConfigParser):
    _instance: Optional["ConfigParser"] = None

    def __new__(cls, *args, **kwargs) -> "ConfigParser":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        del self.__init__
