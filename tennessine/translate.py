from typing import Optional, Dict


class Translate:
    translate: Optional["Translate"] = None
    data: Dict[str, str] = dict()

    def __new__(cls, file_name: str) -> "Translate":
        if not cls.translate:
            cls.translate = super().__new__(cls)
            with open(file_name, "r") as file:
                for line in file.readlines():
                    key, value = line.split("=")
                    cls.translate.data[key.strip()] = value.strip()
        return cls.translate

    def __getitem__(self, key: str) -> str:
        return self.data[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.data[key] = value

    def __deltiem__(self, key: str) -> None:
        del self.data[key]

    def __bool__(self) -> bool:
        return True
