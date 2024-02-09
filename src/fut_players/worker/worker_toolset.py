from threading import Lock


class WorkerToolset:

    def __init__(self, logging_queue, page_complete_notifier, player_page_generator, proxies, request_delay):
        self._logging_queue = logging_queue
        self._page_complete_notifier = page_complete_notifier
        self._player_page_generator = player_page_generator
        self._request_delay = request_delay
        self._lock = Lock()
        self.proxies = proxies

    def add_to_csv_queue(self, player_data):
        return self._logging_queue.put(player_data)

    def notify_of_player_complete(self):
        self._page_complete_notifier.increment()

    @property
    def request_delay(self):
        return self._request_delay

    def get_next_page_url(self):
        self._lock.acquire()
        page_url = self._player_page_generator.get_page_url()
        self._player_page_generator.next_page()
        self._lock.release()
        return page_url
