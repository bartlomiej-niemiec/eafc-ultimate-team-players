class WorkerToolset:

    def __init__(self, logging_queue, page_complete_monitor, player_page_generator, request_delay):
        self._logging_queue = logging_queue
        self._page_complete_monitor = page_complete_monitor
        self._player_page_generator = player_page_generator
        self._request_delay = request_delay

    @property
    def logging_queue(self):
        return self._logging_queue

    @property
    def page_complete_monitor(self):
        return self._page_complete_monitor

    @property
    def player_page_generator(self):
        return self._player_page_generator

    @property
    def request_delay(self):
        return self._request_delay

    def get_next_page_url(self):
        return self._player_page_generator.get_next_page_url()