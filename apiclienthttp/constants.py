# pylint: disable=invalid-name
import re
from enum import Enum
from types import MappingProxyType

HTTP_PATTERN = re.compile(r"^https?://.+")
DEFAULT_QUERY_TIMEOUT = 30


class CUSTOM_ERROR(Enum):  # noqa: N801
    refused = MappingProxyType({"status_code": 1, "text": "Connection Refused"})
    timeout = MappingProxyType({"status_code": 1, "text": "Connection Timeout"})
