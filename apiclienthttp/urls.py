from __future__ import annotations
import typing as t

from .structures import Endpoint
from .utils import trim, is_valid_url

EndpointType = dict[str, str] | list[str] | tuple[str, str] | str


class RestURL:
    strict: bool
    address: str = ''

    __endpoints__: list[Endpoint]

    def __init__(self, address: str | None = None, *, endpoints: EndpointType | None = None, strict: bool = False):
        self.strict = strict
        self.__endpoints__ = Endpoint.parse(endpoints)

        if is_valid_url(address):
            self.address = trim(t.cast(str, address))

    def __call__(self, address: str, *uri_params: str | int, **kwargs: str | int) -> str:

        if not is_valid_url(address):
            address = self.url_for(address, *uri_params)

        return self.set_params(address, **kwargs)

    def set_params(self, url: str, **params: t.Union[str, int]) -> str:
        if not params:
            return url

        return f"{url}?{'&'.join(self.build_param(key, value) for key, value in params.items())}"

    @staticmethod
    def build_param(key, value):
        if isinstance(value, list):
            return '&'.join(('{}={}'.format(key, v) for v in value))  # pylint: disable=consider-using-f-string

        return f'{key}={value}'

    def url_for(self, endpoint: str, *uri_params: t.Union[str, int]) -> str:
        if is_valid_url(target := self.get_endpoint(endpoint).uri.format(*uri_params)):
            return target

        query = [self.address, target]
        if not self.strict:
            query.append("")

        return "/".join(query)

    def has_endpoint(self, name: str) -> bool:
        return any(self._find(name))

    def get_endpoint(self, name: str) -> Endpoint:
        if (result := next(self._find(name), None)) is None:
            raise ValueError(f"Endpoint '{name}' doesn't exists")
        return result

    def add_endpoints(self, endpoints: EndpointType) -> None:
        for endpoint in Endpoint.parse(endpoints):
            if (matched := next(self._find(endpoint.name), None)) is None:
                return self.__endpoints__.append(endpoint)
            matched.uri = endpoint.uri
        return None

    def _find(self, name: str):
        return filter(lambda e: t.cast(Endpoint, e).name == name, self.__endpoints__)
