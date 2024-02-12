from threading import Lock
from utils.config_parser import Config
from utils.proxy_pool import ProxyPool
from utils.proxy_servers import get_proxy_servers_from_file


class WorkerToolset:

    def __init__(self, logging_queue, player_page_generator, config: Config):
        self._logging_queue = logging_queue
        self._player_page_generator = player_page_generator
        self.proxies = None
        self._config = config
        self.proxies = None
        if self._config.use_proxy():
            self.proxies = self._proxies = ProxyPool(
                get_proxy_servers_from_file(
                    self._config.get_proxy_servers_filepath()
                )
            )
        self._lock = Lock()

    def add_to_csv_queue(self, player_data):
        return self._logging_queue.put(player_data)

    def get_request_delay(self):
        return self._config.get_request_delay()

    def get_next_page_url(self):
        self._lock.acquire()
        page_url = self._player_page_generator.get_page_url()
        self._player_page_generator.next_page()
        self._lock.release()
        return page_url

    def get_no_workers(self):
        return self._config.get_no_working_threads()

    def use_proxy(self):
        return self._config.use_proxy()
