from futwiz.players_page.players_page_parser import PlayersPageParser
from futwiz.players_page.players_page_url_generator import PlayerPageUrlFactory
from futwiz.players_page.util import PlayersPageType
from utils.get_requests.get_request_factory import HttpGetRequestFactory
from futwiz.players_page.html_elements_constants.common_html_constants import A_PLAYERS_LIST


class LastPlayersPage:
    _PAGE_START = 733

    def __init__(self, ea_fc_version):
        self.page_url_generator = PlayerPageUrlFactory.create(self._PAGE_START, PlayersPageType.AllPlayers,
                                                              ea_fc_version)
        self.last_page_no = None
        self._number_of_players_in_page = None
        self._get_request = HttpGetRequestFactory.create(None, 3)

    def get_page_number(self):
        no_players_in_last_page = 0
        while no_players_in_last_page := PlayersPageParser(
                self._get_request.get(self.page_url_generator.get_page_url()), A_PLAYERS_LIST).get_players_ref_list():
            self.page_url_generator.next_page()
            self._get_request.get(self.page_url_generator.get_page_url())
        self._number_of_players_in_page = len(no_players_in_last_page)
        return self.page_url_generator.get_page_number() - 1

    def get_no_players(self):
        if self._number_of_players_in_page is None:
            self.get_page_number()
        return self._number_of_players_in_page
