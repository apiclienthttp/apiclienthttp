# pylint: disable=invalid-name
import re
from enum import Enum
from types import MappingProxyType

HTTP_PATTERN = re.compile("^https?://.+")
DEFAULT_QUERY_TIMEOUT = 30


class CUSTOM_ERROR(Enum):
    refused = MappingProxyType({'status_code': 1, 'text': "Connection Refused"})
    timeout = MappingProxyType({'status_code': 1, 'text': "Connection Timeout"})
