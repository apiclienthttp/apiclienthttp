from __future__ import annotations
import typing as t

from .structures import Header


class RestHeaders:
    __headers__: list[Header]

    def __init__(self, *args, **kwargs):
        self.__headers__ = self.create(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        result = {}

        for header in self.__headers__:
            result.update(header.to_dict())
        for header in self.create(*args, **kwargs):
            result.update(header.to_dict())

        return result

    @staticmethod
    def create(*args, **kwargs) -> list[Header]:
        result = Header.parse(kwargs)
        for header in args:
            result.extend(Header.parse(header))
        return result

    def has(self, name) -> bool:
        return any(self._find(name))

    def keys(self) -> list[str]:
        return [h.name for h in self.__headers__]

    def get(self, name: str, default: str | None = None) -> t.Optional[str]:
        if (result := next(self._find(name), None)) is None:
            return default
        return result.value

    def add(self, *args, **kwargs) -> None:
        for header in self.create(*args, **kwargs):
            if (matched := next(self._find(header.name), None)) is None:
                return self.__headers__.append(header)
            matched.value = header.value
        return None

    def _find(self, name: str) -> t.Iterator[Header]:
        return filter(lambda h: t.cast(Header, h).name == name.lower(), self.__headers__)

    def __getitem__(self, name: str) -> str:
        if (result := self.get(name, None)) is None:
            raise KeyError(name)
        return result

    def __setitem__(self, name: str, value: str) -> None:
        return self.add({name: value})
