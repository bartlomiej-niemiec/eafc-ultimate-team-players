import time
import requests
from utils.proxy_pool import ProxyPool
from enum import Enum

REQUEST_DELAY = 2.5


class GetRequest:

    def __init__(self, proxy_pool: ProxyPool, delay=REQUEST_DELAY):
        self.error_code = None
        self.error_msg = None
        self._no_retries = None
        self._proxy_pool = proxy_pool
        self._delay = delay
        self._html_text = None

    @property
    def no_retries(self):
        return self._no_retries

    @no_retries.setter
    def no_retries(self, num):
        self._no_retries = num

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, delay_in_s):
        self._delay = delay_in_s

    def send(self, url, with_proxy=False, with_delay=False):
        self._html_text = None
        self.error_code = 0
        self.error_msg = ""
        self._get_request_with_retries(url, self.no_retries, with_proxy, with_delay)
        return True if not self.error_code else False

    def get_page_html_text(self):
        return self._html_text

    def _get_request_with_retries(self, url, no_retries, with_proxy=False, with_delay=False):
        while no_retries:
            if with_delay:
                time.sleep(REQUEST_DELAY)
            try:
                proxy = None
                if with_proxy:
                    proxy = self._proxy_pool.alloc()
                response = requests.get(url, proxies=proxy)
                if proxy:
                    self._proxy_pool.dealloc(proxy)
                response.raise_for_status()
                self._html_text = response.text
                break
            except requests.exceptions.HTTPError:
                status_code = response.status_code
                if status_code == ErrorCode.HTTP_NOT_FOUND:
                    self.error_msg = f"Requested address: {url} not found: HTTP 404 error"
                    self.error_code = ErrorCode.HTTP_NOT_FOUND
                    break
                else:
                    no_retries -= 1
                    if no_retries == 0:
                        self.error_msg = f"Request failed {self.no_retries} times for address: {url}"
                        self.error_code = ErrorCode.MAX_RETRIES


class ErrorCode(Enum):
    MAX_RETRIES = 1
    HTTP_NOT_FOUND = 404
