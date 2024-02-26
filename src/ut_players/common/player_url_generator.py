from threading import Lock
from futwiz.player_page.player_data_template import GeneralPlayerData


class PlayerUrlGenerator:

    def __init__(self, csv_content):
        self._csv_content = csv_content
        self._current_row = 1
        self._lock = Lock()

    def get_next_url(self):
        self._lock.acquire()
        try:
            url = self._csv_content[GeneralPlayerData.FutwizLink].iloc[self._current_row]
        except IndexError:
            url = None
        self._current_row += 1
        self._lock.release()
        return url
