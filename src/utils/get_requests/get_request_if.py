from abc import ABC, abstractmethod


class HttpGetRequest(ABC):
    _DEFAULT_DELAY = 3

    def __init__(self):
        self.status_code = None

    @abstractmethod
    def get(self, page_url, delay_in_s=None):
        pass

    def get_status_code(self):
        return self.status_code
