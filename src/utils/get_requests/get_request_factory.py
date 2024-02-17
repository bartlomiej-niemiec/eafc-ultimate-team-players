from utils.get_requests.error_handler_decorator import ErrorHandlerDecorator
from utils.get_requests.get_request import ProxyRequest, StandardRequest
from utils.get_requests.retry_decorator import RetryDecorator


class HttpGetRequestFactory:

    @classmethod
    def create(cls, proxy_pool, max_retries):
        get_request = None
        if proxy_pool:
            get_request = RetryDecorator(ErrorHandlerDecorator(ProxyRequest(proxy_pool)), max_retries)
        else:
            get_request = RetryDecorator(ErrorHandlerDecorator(StandardRequest()), max_retries)
        return get_request
