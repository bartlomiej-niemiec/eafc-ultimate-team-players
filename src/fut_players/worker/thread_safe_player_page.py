from multiprocessing import Lock
from futwiz.players_page.futwiz_players_page_url import PlayersPageUrlGenerator


class TSPlayersPageUrlGenerator(PlayersPageUrlGenerator):

    def __init__(self, start_page_no):
        self._lock = Lock()
        super(TSPlayersPageUrlGenerator, self).__init__(start_page_no)

    def next_page(self):
        self._lock.acquire()
        self._current_page += 1
        self._lock.release()

    def get_page_url(self):
        self._lock.acquire()
        page_url = super().get_page_url()
        self._lock.release()
        return page_url

    def get_page_number(self):
        self._lock.acquire()
        current_page = super().get_page_number()
        self._lock.acquire()
        return current_page
