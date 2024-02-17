from futwiz.players_page.constants import FUTWIZ_PLAYERS_URL, FUTWIZ_LATEST_PLAYERS_URL
from futwiz.players_page.util import PlayersPageType


class PlayerPageUrlFactory:

    @classmethod
    def create(cls, start_page, players_page_type: PlayersPageType):
        if players_page_type == PlayersPageType.AllPlayers:
            return PlayersPageUrlGenerator(start_page, FUTWIZ_PLAYERS_URL)
        elif players_page_type == PlayersPageType.LatestAddedPlayers:
            return PlayersPageUrlGenerator(0, FUTWIZ_LATEST_PLAYERS_URL)


class PlayersPageUrlGenerator:

    def __init__(self, start_page_no, players_url):
        self._current_page = start_page_no
        self._players_url = players_url

    def next_page(self):
        self._current_page += 1

    def get_page_url(self):
        return self._players_url.format(page_number=self._current_page)

    def get_page_number(self):
        return self._current_page
