# coding:utf-8

import os
from typing import Any
from typing import Dict

from toml import dumps
from toml import loads

from xlc.database.langtags import LangItem
from xlc.database.langtags import LangT
from xlc.database.langtags import LangTags


class Context():
    def __init__(self, language: str):
        self.__datas: Dict[str, Any] = {"language": language}

    def get(self, index: str) -> Any:
        return self.__datas[index]

    def set(self, index: str, value: Any):
        self.__datas[index] = value

    def all(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__datas.items()}

    def fill(self, **kwargs: Any) -> Dict[str, str]:
        return {k: v.format(**kwargs) if isinstance(v, str) else str(v)
                for k, v in self.__datas.items()}


class Section(Context):
    def __init__(self, language: LangItem, title: str = ""):
        super().__init__(language.name)
        self.__sections: Dict[str, Section] = {}
        self.__language: LangItem = language
        self.__title: str = title

    @property
    def lang(self) -> LangItem:
        return self.__language

    def init(self, index: str, value: Any):
        if isinstance(value, dict):
            for k, v in value.items():
                self.seek(index).init(k, v)
        else:
            self.set(index, value)

    def seek(self, index: str) -> "Section":
        section: Section = self
        for key in index.split("."):
            section = section.find(key)
        return section

    def find(self, index: str) -> "Section":
        if index not in self.__sections:
            title: str = ".".join([self.__title, index])
            section = Section(language=self.lang, title=title)
            self.__sections.setdefault(index, section)
        return self.__sections[index]

    def dump(self) -> Dict[str, Dict[str, Any]]:
        datas: Dict[str, Any] = self.all()
        for k, v in self.__sections.items():
            datas[k] = v.dump()
        return datas


class Segment(Section):
    def __init__(self, language: LangItem):
        super().__init__(language=language)

    def dumps(self) -> str:
        return dumps(self.dump())

    def dumpf(self, file: str) -> None:
        with open(file, "w", encoding="utf-8") as whdl:
            whdl.write(self.dumps())

    @classmethod
    def load(cls, lang: LangItem, data: Dict[str, Any]) -> "Segment":
        instance: Segment = cls(lang)
        for k, v in data.items():
            instance.init(k, v)
        return instance

    @classmethod
    def loads(cls, lang: LangItem, data: str) -> "Segment":
        return cls.load(lang=lang, data=loads(data))

    @classmethod
    def loadf(cls, file: str) -> "Segment":
        with open(file, "r", encoding="utf-8") as rhdl:
            langtags: LangTags = LangTags.from_config()
            base: str = os.path.basename(file)
            ltag: str = base[:base.find(".")]
            data: str = rhdl.read()
            return cls.loads(lang=langtags[ltag], data=data)

    @classmethod
    def generate(cls, langtag: LangT) -> "Segment":
        lang: LangItem = LangTags.from_config()[langtag]
        return Segment.load(lang, {})
