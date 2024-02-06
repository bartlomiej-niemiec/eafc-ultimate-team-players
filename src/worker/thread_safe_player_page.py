from multiprocessing import Lock
from futwiz.players_page.futwiz_players_page_url import PlayersPageUrl


class SafePlayersPageUrl(PlayersPageUrl):

    def __init__(self):
        self._lock = Lock()
        super(SafePlayersPageUrl, self).__init__()

    def get_next_page_url(self):
        self._lock.acquire()
        page_url = super().get_next_page_url()
        self._lock.release()
        return page_url
