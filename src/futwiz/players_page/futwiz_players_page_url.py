class PlayersPageUrl:

    _URL = "https://www.futwiz.com/en/fc24/players?page={page_number}"

    def __init__(self):
        self._current_page = 0

    def get_next_page_url(self):
        self._current_page += 1
        return self._URL.format(page_number=self._current_page)