from threading import Lock
from utils.proxy_pool import ProxyPool
from utils.proxy_servers import get_proxy_servers_from_file
import config


class WorkerToolset:

    def __init__(self, logging_queue, player_page_generator):
        self._logging_queue = logging_queue
        self._player_page_generator = player_page_generator
        self.proxies = None
        if config.USE_PROXY:
            self.proxies = self._proxies = ProxyPool(
                get_proxy_servers_from_file(
                    config.PROXY_SERVERS_FILE_PATH
                )
            )
        self._lock = Lock()

    def add_to_csv_queue(self, player_data):
        return self._logging_queue.put(player_data)

    def get_request_delay(self):
        return config.DELAY_BETWEEN_REQUESTS_S

    def get_next_page_url(self):
        self._lock.acquire()
        page_url = self._player_page_generator.get_page_url()
        self._player_page_generator.next_page()
        self._lock.release()
        return page_url

    def use_proxy(self):
        return config.USE_PROXY
