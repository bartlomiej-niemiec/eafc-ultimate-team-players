import time
import requests

from utils.get_requests.get_request_if import HttpGetRequest


class ProxyRequest(HttpGetRequest):

    def __init__(self, proxy_pool):
        super().__init__()
        self._proxy_pool = proxy_pool

    def get(self, page_rul, delay_in_s=None):
        if delay_in_s:
            time.sleep(delay_in_s)
        proxy_servers = self._proxy_pool.alloc()
        response = requests.get(page_rul, proxies=proxy_servers)
        self.status_code = response.status_code
        self._proxy_pool.dealloc(proxy_servers)
        return response


class StandardRequest(HttpGetRequest):

    def __init__(self):
        super().__init__()

    def get(self, page_rul, delay_in_s=None):
        if delay_in_s:
            time.sleep(delay_in_s)
        response = requests.get(page_rul)
        self.status_code = response.status_code
        return response