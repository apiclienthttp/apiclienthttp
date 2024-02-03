from httpx import TimeoutException, NetworkError

__all__ = [
    'TimeoutException',
    'NetworkError'
]


class RestQueryError(Exception):
    name: str
    code: int

    def __init__(self, *args, name: str | None = None, code: int | None = None):
        super().__init__(*args)
        self.name = name if name is not None else type(self).__name__
        self.code = code if code is not None else 0

    def __str__(self):
        return f'{self.name} Error: {self.message} ({self.code})'

    @property
    def message(self):
        return "\n".join(self.args)
