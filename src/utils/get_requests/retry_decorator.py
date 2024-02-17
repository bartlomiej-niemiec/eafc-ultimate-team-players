from src.utils.get_requests.exceptions import HTTPGetRequestFailed
from src.utils.get_requests.get_request_if import HttpGetRequest
from src.utils.get_requests.error_handler_decorator import ErrorHandlerDecorator
from http import HTTPStatus


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
            self.status_code = self._http_request.status_code
            if self._http_request.status_code == HTTPStatus.NOT_FOUND:
                self.status_code = HTTPStatus.NOT_FOUND
                break
            elif self._http_request.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                no_left_retries -= 1
                self.status_code = HTTPStatus.TOO_MANY_REQUESTS
                if no_left_retries == 0:
                    break
            elif self._http_request.status_code == HTTPStatus.OK:
                break
            else:
                raise HTTPGetRequestFailed(f"Request has finished with status code: {self._http_request.status_code}")
        return response.text
