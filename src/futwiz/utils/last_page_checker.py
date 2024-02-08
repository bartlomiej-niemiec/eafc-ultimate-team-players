from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.players_page.futwiz_players_page_url import PlayersPageUrlGenerator

# 710 was the last page on 07.02.2023
PAGE_START = 710


class PlayersLastPage:

    def __init__(self):
        self.page_url_generator = PlayersPageUrlGenerator(PAGE_START)
        self.last_page_no = None
        self._number_of_players_in_page = None

    def get_last_page_number(self):
        if not self.last_page_no:
            number_of_players_in_page = None
            while _ := PlayersPage(self.page_url_generator.get_next_page_url()).get_players_ref_list():
                number_of_players_in_page = _
            self._number_of_players_in_page = len(number_of_players_in_page)
        return self.page_url_generator.get_page_number() - 1

    def get_number_of_players(self):
        return self._number_of_players_in_page

