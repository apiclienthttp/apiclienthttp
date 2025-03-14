from __future__ import annotations

import typing as t

from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field as f
from itertools import starmap
from types import MappingProxyType

from .utils import trim


@dataclass
class Endpoint:
    name: str
    uri: str

    @classmethod
    def create(cls, name: str, uri: str) -> Endpoint:
        return cls(name=name, uri=trim(uri))

    @classmethod
    def parse(cls, endpoint: dict[str, str] | list[str] | tuple[str, str] | str | None) -> list[Endpoint]:
        if isinstance(endpoint, dict | MappingProxyType):
            return list(starmap(cls.create, endpoint.items()))
        if isinstance(endpoint, tuple | list) and len(endpoint) == 2:  # noqa: PLR2004
            return [cls.create(*endpoint)]
        if isinstance(endpoint, str):
            return [cls.create(endpoint, endpoint)]
        return []


@dataclass
class Header:
    name: str
    display: str
    value: str

    @classmethod
    def create(cls, display: str, value: str) -> Header:
        return cls(name=display.lower(), display=display, value=value)

    @classmethod
    def parse(cls, header: dict[str, str] | list[str] | tuple[str, str]) -> list[Header]:
        if isinstance(header, dict | MappingProxyType):
            return list(starmap(Header.create, header.items()))
        if isinstance(header, tuple | list) and len(header) == 2:  # noqa: PLR2004
            return [Header.create(*header)]
        return []

    def to_dict(self) -> dict[str, str]:
        return {self.display: self.value}


@dataclass
class Options:
    full_response: bool = f(default=False)
    ok_codes: list[int] = f(default_factory=list)
    bypass: dict[str, t.Any] = f(default_factory=dict)

    @classmethod
    def create(cls, full_response: bool | None = None, ok_codes: int | list[int] | tuple[int, ...] | None = None, **bypass) -> Options:
        result = cls(bypass=bypass, ok_codes=cls._parse_code(ok_codes))

        if isinstance(full_response, bool):
            result.full_response = full_response

        return result

    @staticmethod
    def _parse_code(code: int | list[int] | tuple[int, ...] | None) -> list[int]:
        if isinstance(code, int):
            return [code]
        if isinstance(code, list | tuple):
            return list(code)
        return [200]

    def clone(self) -> Options:
        return Options(full_response=self.full_response, ok_codes=self.ok_codes.copy(), bypass=deepcopy(self.bypass))

    def merge(self, **overrides) -> Options:
        result = self.clone()

        if "full_response" in overrides:
            result.full_response = bool(overrides.pop("full_response"))
        if "ok_codes" in overrides:
            result.ok_codes = self._parse_code(overrides.pop("ok_codes"))
        if overrides:
            result.bypass.update(overrides)

        return result
