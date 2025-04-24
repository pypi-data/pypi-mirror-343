# coding:utf-8

import os
from typing import Dict
from typing import Optional

BASE: str = os.path.dirname(__file__)


class Stag():
    def __str__(self) -> str:
        return self.code

    @property
    def code(self) -> str:
        raise NotImplementedError()

    @classmethod
    def get(cls, base: str, name: str) -> Dict[str, str]:
        from toml import load

        path: str = os.path.join(base, name.lower())
        if os.path.isfile(path):
            with open(path, "r", encoding="UTF-8") as rhdl:
                return load(rhdl)
        else:
            raise KeyError(f"{path} is not found")


class Language(Stag):
    """Language in ISO 639-3"""
    CONFIG: str = os.path.join(BASE, "languages")

    def __init__(self, data: Dict[str, str]):
        self.__alpha_2: Optional[str] = data.get("alpha_2")
        self.__alpha_3: str = data["alpha_3"]
        self.__name: str = data["name"]

    @property
    def code(self) -> str:
        return self.alpha_2 or self.alpha_3

    @property
    def name(self) -> str:
        return self.__name

    @property
    def alpha_2(self) -> Optional[str]:
        return self.__alpha_2

    @property
    def alpha_3(self) -> str:
        return self.__alpha_3

    @classmethod
    def get(cls, index: str) -> "Language":
        return cls(super().get(cls.CONFIG, index))


class Region(Stag):
    """Country or Region in ISO 3166-1"""
    CONFIG: str = os.path.join(BASE, "regions")

    def __init__(self, data: Dict[str, str]):
        self.__official_name: str = data["official_name"]
        self.__alpha_2: str = data["alpha_2"]
        self.__alpha_3: str = data["alpha_3"]
        self.__numeric: str = data["numeric"]
        self.__flag: str = data["flag"]
        self.__name: str = data["name"]

    @property
    def code(self) -> str:
        return self.alpha_2

    @property
    def name(self) -> str:
        return self.__name

    @property
    def flag(self) -> str:
        return self.__flag

    @property
    def numeric(self) -> int:
        return int(self.__numeric)

    @property
    def alpha_2(self) -> str:
        return self.__alpha_2

    @property
    def alpha_3(self) -> str:
        return self.__alpha_3

    @property
    def official_name(self) -> str:
        return self.__official_name

    @classmethod
    def get(cls, index: str) -> "Region":
        return cls(super().get(cls.CONFIG, index))


class Script(Stag):
    """Script in ISO 15924"""
    CONFIG: str = os.path.join(BASE, "scripts")

    def __init__(self, data: Dict[str, str]):
        self.__alpha_4: str = data["alpha_4"]
        self.__numeric: str = data["numeric"]
        self.__name: str = data["name"]

    @property
    def code(self) -> str:
        return self.alpha_4

    @property
    def name(self) -> str:
        return self.__name

    @property
    def numeric(self) -> int:
        return int(self.__numeric)

    @property
    def alpha_4(self) -> str:
        return self.__alpha_4

    @classmethod
    def get(cls, index: str) -> "Script":
        return cls(super().get(cls.CONFIG, index))
