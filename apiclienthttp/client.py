from __future__ import annotations
import typing as t

from json import dumps
from types import MappingProxyType
import httpx

from .structures import Options
from .response import RestResponse, ErrorResponse
from .headers import RestHeaders
from .urls import RestURL
from .exceptions import RestQueryError, TimeoutException, NetworkError
from .constants import CUSTOM_ERROR


class BaseRestClient:
    name: str

    def __init__(self, address=None, endpoints=None, headers=None, strict=False, **kwargs):
        self.url = RestURL(address, endpoints=endpoints, strict=strict)
        self.headers = RestHeaders(**headers) if isinstance(headers, (dict, MappingProxyType)) else RestHeaders()
        self.options = Options.create(**kwargs)

    def output(self, response: RestResponse, options: Options):
        if not response.is_ok(options.ok_codes):
            raise RestQueryError(
                self.parse_response_error(response),
                name=getattr(self, 'name', type(self).__name__),
                code=response.status_code,
            )

        if options.full_response or int(response.headers.get('Content-Length', '0')) <= 1:
            return response

        return response.content

    @staticmethod
    def _extract_data(data=None, json=None):
        if data is None and json is not None:
            data = dumps(json)
        return data

    @staticmethod
    def parse_response_error(response: RestResponse) -> str:
        if isinstance((content := response.content), str):
            return content

        if isinstance(content, dict):
            if content.get('message'):
                return content['message']
            if content.get('error'):
                return content['error']

        return response.text


class RestClient(BaseRestClient):
    name: str

    def __call__(self,
                 method,
                 *address,
                 params: dict[str, t.Any] | None = None,
                 json: dict | list | None = None,
                 data: t.Any = None,
                 headers: dict[str, str] | None = None,
                 **opts):
        if len(address) == 0:
            raise ValueError("Address not set")

        params = params if isinstance(params, dict) else {}
        headers = headers if isinstance(headers, dict) else {}
        options = self.options.merge(**opts)

        return self.output(
            self.send(
                method=method.upper(),
                url=self.url(*address, **params),
                headers=self.headers(**headers),
                data=self._extract_data(data, json),
                options=options
            ),
            options
        )

    @staticmethod
    def send(method: str, url: str, headers: dict, data: t.Any, options: Options) -> RestResponse:
        try:
            return RestResponse(httpx.request(method, url, headers=headers, data=data, **options.bypass))
        except NetworkError:
            return RestResponse(ErrorResponse(url, **CUSTOM_ERROR.refused.value))
        except TimeoutException:
            return RestResponse(ErrorResponse(url, **CUSTOM_ERROR.timeout.value))


class AsyncRestClient(BaseRestClient):
    name: str

    async def __call__(self,
                       method,
                       *address,
                       params: dict[str, t.Any] | None = None,
                       json: dict | list | None = None,
                       data: t.Any = None,
                       headers: dict[str, str] | None = None,
                       **opts):
        if len(address) == 0:
            raise ValueError("Address not set")

        params = params if isinstance(params, dict) else {}
        headers = headers if isinstance(headers, dict) else {}
        options = self.options.merge(**opts)

        return self.output(
            await self.send(
                method=method.upper(),
                url=self.url(*address, **params),
                headers=self.headers(**headers),
                data=self._extract_data(data, json),
                options=options
            ),
            options
        )

    @staticmethod
    async def send(method: str, url: str, headers: dict, data: t.Any, options: Options) -> RestResponse:
        client = httpx.AsyncClient()
        try:
            return RestResponse(await client.request(method, url, headers=headers, data=data, **options.bypass))
        except NetworkError:
            return RestResponse(ErrorResponse(url, **CUSTOM_ERROR.refused.value))
        except TimeoutException:
            return RestResponse(ErrorResponse(url, **CUSTOM_ERROR.timeout.value))
        finally:
            await client.aclose()
