class PlayersPageUrlGenerator:
    _URL = "https://www.futwiz.com/en/fc24/players?page={page_number}"

    def __init__(self, start_page_no):
        self._current_page = start_page_no
        self._last_page_number = start_page_no

    def get_next_page_url(self):
        self._last_page_number = self._current_page
        page_url = self._URL.format(page_number=self._current_page)
        self._current_page += 1
        return page_url

    def get_page_number(self):
        return self._last_page_number
