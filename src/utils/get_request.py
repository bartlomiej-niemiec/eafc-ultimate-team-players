import time
from abc import ABC, abstractmethod
import requests
from enum import Enum


class HttpGetRequestFactory:

    @classmethod
    def create(cls, proxy_pool, max_retries):
        get_request = None
        if proxy_pool:
            get_request = RetryDecorator(ErrorHandlerDecorator(ProxyPoolRequest(proxy_pool)), max_retries)
        else:
            get_request = RetryDecorator(ErrorHandlerDecorator(StandardRequest()), max_retries)
        return get_request


class HttpGetRequest(ABC):
    _DEFAULT_DELAY = 3
    _REQUEST_SUCCESS = 200
    def __init__(self):
        self._error_code = None

    @abstractmethod
    def get(self, page_url, delay_in_s=None):
        pass

    def get_error_code(self):
        return self._error_code


class ProxyPoolRequest(HttpGetRequest):

    def __init__(self, proxy_pool):
        super().__init__()
        self._proxy_pool = proxy_pool

    def get(self, page_rul, delay_in_s=None):
        if delay_in_s:
            time.sleep(delay_in_s)
        proxy_servers = self._proxy_pool.alloc()
        response = requests.get(page_rul, proxies=proxy_servers)
        self._error_code = response.status_code
        self._proxy_pool.dealloc(proxy_servers)
        return response


class StandardRequest(HttpGetRequest):

    def __init__(self):
        super().__init__()

    def get(self, page_rul, delay_in_s=None):
        if delay_in_s:
            time.sleep(delay_in_s)
        response = requests.get(page_rul)
        self._error_code = response.status_code
        return response


class ErrorHandlerDecorator(HttpGetRequest):

    def __init__(self, http_request):
        super().__init__()
        self._http_request = http_request

    def get(self, page_rul, delay_in_s=None):
        self.error_code = None
        response = self._http_request.get(page_rul, delay_in_s)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.error_code = response.status_code
        finally:
            return response


class RetryDecorator(HttpGetRequest):

    def __init__(self, http_request: ErrorHandlerDecorator, max_retries=0):
        super().__init__()
        self._http_request = http_request
        self.max_retries = max_retries

    def get(self, page_rul, delay_in_s=None):
        no_left_retries = self.max_retries
        delay = delay_in_s
        while True:
            if delay is None and no_left_retries != self.max_retries:
                delay = self._DEFAULT_DELAY
            response = self._http_request.get(page_rul, delay)
            if self._http_request.error_code:
                if self._http_request.error_code == ErrorCode.HTTP_NOT_FOUND:
                    self._error_code = ErrorCode.HTTP_NOT_FOUND
                    break
                elif self._http_request.error_code == ErrorCode.TO_MANY_REQUEST:
                    no_left_retries -= 1
                    self._error_code = ErrorCode.TO_MANY_REQUEST
                    if no_left_retries == 0:
                        break
            elif self._http_request.error_code is None or self._http_request.error_code == self._REQUEST_SUCCESS:
                break
        return response.text


class ErrorCode(Enum):
    NO_ERROR = None
    MAX_RETRIES = 1
    HTTP_NOT_FOUND = 404
    TO_MANY_REQUEST = 429
