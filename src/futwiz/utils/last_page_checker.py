from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.players_page.futwiz_players_page_url import PlayersPageUrlGenerator
from utils.get_requests import GetRequest

# 710 was the last page on 07.02.2023
PAGE_START = 723


class PlayersLastPage:

    def __init__(self):
        self.page_url_generator = PlayersPageUrlGenerator(PAGE_START)
        self.last_page_no = None
        self._number_of_players_in_page = None
        self._get_request = GetRequest(None)
        self._get_request.no_retries = 3

    def get_last_page_number(self):
        number_of_players_in_page = None
        while _ := PlayersPage(self.page_url_generator.get_page_url(), self._get_request, False).get_players_ref_list():
            number_of_players_in_page = _
            self.page_url_generator.next_page()
        self._number_of_players_in_page = len(number_of_players_in_page)
        return self.page_url_generator.get_page_number() - 1

    def get_number_of_players(self):
        return self._number_of_players_in_page

