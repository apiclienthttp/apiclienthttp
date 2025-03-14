from __future__ import annotations

from .constants import HTTP_PATTERN


def trim(url: str) -> str:
    if url[0] == "/":
        url = url[1:]
    if url[-1] == "/":
        url = url[:-1]
    return url


def is_valid_url(url: str | None) -> bool:
    if not isinstance(url, str):
        return False
    return bool(HTTP_PATTERN.match(url))
