import requests
from utils.get_requests.get_request_if import HttpGetRequest
from http import HTTPStatus


class ErrorHandlerDecorator(HttpGetRequest):

    def __init__(self, http_request):
        super().__init__()
        self._http_request = http_request

    def get(self, page_rul, delay_in_s=None):
        self.status_code = HTTPStatus.OK
        response = self._http_request.get(page_rul, delay_in_s)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.status_code = response.status_code
        finally:
            return response
