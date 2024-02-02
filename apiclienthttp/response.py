from json import dumps

from httpx import Response

from .baseclasses import BaseResponse
from .headers import RestHeaders


class RestResponse(BaseResponse):
    _raw = None

    def __init__(self, response):
        self._raw = response

        if not isinstance(response, (Response, ErrorResponse)):
            raise ValueError(f'Responce argument must be instance of {Response}')

        self._headers = RestHeaders(**dict(response.headers))

    def is_ok(self, codes):
        return self.status_code in codes

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, _):
        raise TypeError(f"Can't change response in {type(self)}")

    @property
    def status_code(self):
        return self._raw.status_code

    @property
    def content(self):
        if self.headers.get('content-type', '').find('application/json') != -1:
            return self.json()

        return self.text

    @property
    def url(self):
        return self._raw.url

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, _):
        raise TypeError(f"Can't change headers in {type(self)}")

    def json(self):
        return self._raw.json()

    @property
    def text(self):
        return self.raw.text


class ErrorResponse(BaseResponse):

    def __init__(self, url, *_, **kwargs):
        self.url = url
        self.headers = RestHeaders(**kwargs.get('headers', {}))
        self.status_code = kwargs.get('status_code', None)
        self._text = kwargs.get('text', None)
        self._json = kwargs.get('json', None)

    def json(self):
        if self._json is not None:
            return self._json

        return dumps(self._text)

    @property
    def text(self):
        return self._text
