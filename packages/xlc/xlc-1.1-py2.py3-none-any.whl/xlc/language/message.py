# coding:utf-8

import os
from typing import Dict
from typing import Iterator

from xlc.database.langtags import LangDict
from xlc.database.langtags import LangItem
from xlc.database.langtags import LangT
from xlc.database.langtags import LangTag
from xlc.database.langtags import LangTags
from xlc.language.segment import Segment


class Message():
    SUFFIX: str = ".xlc"

    def __init__(self, base: str):
        self.__objects: Dict[str, Segment] = {}
        self.__languages: LangDict = LangDict()
        self.__segments: Dict[str, str] = {}

        langtags: LangTags = LangTags.from_config()
        for file in os.listdir(base):
            key, ext = os.path.splitext(file)
            if ext == self.SUFFIX and os.path.isfile(path := os.path.join(base, file)):  # noqa:E501
                lang: LangItem = langtags[key]
                for atag in lang.aliases:
                    self.__segments.setdefault(atag, path)
                self.__segments[lang.name] = path

    def __iter__(self) -> Iterator[str]:
        return iter(self.__segments)

    def __len__(self) -> int:
        return len(self.__segments)

    def __contains__(self, langtag: LangT) -> bool:
        return self.languages.get(langtag).name in self.__segments

    def __getitem__(self, langtag: LangT) -> Segment:
        return self.load(self.languages.get(langtag))

    @property
    def languages(self) -> LangDict:
        return self.__languages

    def lookup(self, langtag: LangT) -> Segment:
        ltag: LangTag = self.languages.get(langtag)
        if ltag.name in self.__segments:
            return self.load(ltag)
        for _tag in ltag.tags:
            ltag = self.languages[_tag]
            if ltag.name in self.__segments:
                return self.load(ltag)
        raise LookupError(f"No such language tag: {langtag}")

    def load(self, ltag: LangTag) -> Segment:
        path: str = self.__segments[ltag.name]
        if path not in self.__objects:
            segment: Segment = Segment.loadf(path)
            self.__objects[path] = segment
        return self.__objects[path]
