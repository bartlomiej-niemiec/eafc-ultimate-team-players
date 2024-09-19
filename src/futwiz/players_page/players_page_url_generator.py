from futwiz.players_page.util import PlayersPageType
from futwiz.players_page.html_elements_constants.html_elements_provider import HtmlElementsProvider


class PlayerPageUrlFactory:

    @classmethod
    def create(cls, start_page, players_page_type: PlayersPageType, ea_fc_version):
        if players_page_type == PlayersPageType.AllPlayers:
            futwiz_players_url = HtmlElementsProvider.get_html_constants(ea_fc_version).FUTWIZ_PLAYERS_URL
            return PlayersPageUrlGenerator(start_page, futwiz_players_url)
        elif players_page_type == PlayersPageType.LatestAddedPlayers:
            futwiz_players_url = HtmlElementsProvider.get_html_constants(ea_fc_version).FUTWIZ_LATEST_PLAYERS_URL
            return PlayersPageUrlGenerator(0, futwiz_players_url)


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
