import time
import requests
from utils.proxy_servers import ProxyPool
from enum import Enum

DEFAULT_REQUEST_DELAY = 2.5


class GetRequest:

    def __init__(self, proxy_pool: ProxyPool, max_retries, delay_to_retry=DEFAULT_REQUEST_DELAY):
        self.error_code = None
        self._proxy_pool = proxy_pool
        self._delay_to_retry = delay_to_retry
        self._max_retries = max_retries
        self._html_text = None

    @property
    def delay_to_retry(self):
        return self._delay_to_retry

    @delay_to_retry.setter
    def delay_to_retry(self, delay_in_s):
        self._delay_to_retry = delay_in_s

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, no_retries):
        self._max_retries = no_retries

    def send(self, url,  user_proxy_server=False):
        self._clear_state()
        self._get_request_with_retries(url, user_proxy_server)
        return self._html_text if not self.error_code else None

    def _clear_state(self):
        self._html_text = None
        self.error_code = 0

    def _get_request_with_retries(self, url, user_proxy_server=False):
        retries_left = self._max_retries
        proxy_server = None
        while retries_left:
            if retries_left != self._max_retries:
                time.sleep(self._delay_to_retry)
            try:
                proxy_server = None
                if user_proxy_server:
                    proxy_server = self._proxy_pool.alloc()
                response = requests.get(url, proxies=proxy_server)
                if proxy_server:
                    self._proxy_pool.dealloc(proxy_server)
                response.raise_for_status()
                source = response.text
                self._html_text = source
                break
            except requests.exceptions.HTTPError:
                status_code = response.status_code
                if status_code == ErrorCode.HTTP_NOT_FOUND:
                    self.error_code = ErrorCode.HTTP_NOT_FOUND
                    break
                else:
                    if retries_left == 0:
                        self.error_code = ErrorCode.MAX_RETRIES
                    retries_left -= 1
            finally:
                if proxy_server:
                    self._proxy_pool.dealloc(proxy_server)


class ErrorCode(Enum):
    MAX_RETRIES = 1
    HTTP_NOT_FOUND = 404
