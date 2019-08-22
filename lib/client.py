from time import sleep
from typing import Any
from typing import Callable
from typing import Dict  # noqa: F401
from typing import Tuple # noqa: F401
from typing import Optional

from .exceptions import TimeoutException

import json
import logging
import os
import sys
import requests

Response = requests.models.Response

DEFAULT_LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "DEBUG").upper())
DEFAULT_REQUEST_LOG_LEVEL = getattr(logging, os.environ.get("REQUEST_LOG_LEVEL",
                                                            "WARNING").upper())

logger: Any = logging.getLogger(__name__)
logger.setLevel(DEFAULT_LOG_LEVEL)

requests_log = logging.getLogger("urllib3")
requests_log.setLevel(DEFAULT_REQUEST_LOG_LEVEL)
requests_log.propagate = True

ch: Any = logging.StreamHandler(sys.stdout)
ch.setLevel(DEFAULT_LOG_LEVEL)

logger.addHandler(ch)
requests_log.addHandler(ch)

class HTTPClient(object):
    def __init__(self, retries=1, connection_time_out=10, read_time_out=30):
        self._retries = retries
        self._ctime = connection_time_out
        self._rtime = read_time_out

    def request(self,
                method: Callable[..., Response],
                url: str,
                auth: Optional[Tuple] = None,
                data: Optional[str] = None,
                headers: Optional[Dict[str, str]] = None,
                max_retries: Optional[int] = 1,
                connection_timeout_seconds: Optional[int] = 3,
                read_timeout_seconds: Optional[int] = 10,
                ) -> Response:
        _retries = self._retries if (not max_retries or max_retries < 0) else max_retries
        _ctime = self._ctime if (not connection_timeout_seconds or connection_timeout_seconds < 0) else connection_timeout_seconds
        _rtime = self._rtime if (not read_timeout_seconds or read_timeout_seconds < 0) else read_timeout_seconds

        req = requests.Request('POST', url=url, auth=auth, data=data)
        prepped = req.prepare()
        print("header:", prepped.headers)
        print("body:", prepped.body)
        for retry_countdown in range(_retries, 0, -1):
            try:
                r: Response = method(url=url, auth=auth, data=data, headers=headers, timeout=(_ctime, _rtime))
                r.raise_for_status()
                break
            except Exception as e:
                if isinstance(e, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)):
                    if retry_countdown == 1:
                        raise TimeoutException()
                    else:
                        sleep(1.0)
                else:
                    raise e
        return r
