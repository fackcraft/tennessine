import enum
import pathlib

from typing import Dict, Optional

root: pathlib.Path = pathlib.Path(__file__).parent.parent


class Language(enum.Enum):
    en_us = 0
    zh_cn = 1


class Translator:
    _instance: Optional["Translator"] = None
    _data: Dict[str, str] = dict()
    _language: Language = Language.en_us

    def __new__(cls) -> "Translator":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_language()
        return cls._instance

    def __getitem__(self, key: str) -> str:
        print(self._data)
        return self._data[key]

    def __setitem__(self, key: str, value: str) -> None:
        self._data[key] = value

    def __deltiem__(self, key: str) -> None:
        del self._data[key]

    def _load_language(self) -> None:
        language: str = (
            "en_us.lang" if self._language == Language.en_us else "zh_cn.lang"
        )
        with open(root / "config" / "lang" / language, "r") as file:
            while True:
                line: str = file.readline()
                if not line:
                    return
                if "=" not in line:
                    continue
                key, value = line.split("=")
                self._data[key.strip()] = value.strip()
