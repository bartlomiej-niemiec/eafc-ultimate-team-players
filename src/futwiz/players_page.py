from bs4 import BeautifulSoup
from futwiz.constants import FUTWIZ_BASE_URL, A_PLAYERS_LIST
from futwiz.player_page import GeneralPlayerData
from utils.constants import SOUP_HTML_PARSER, A_TAG
from utils.get_request import HttpGetRequestFactory


class PlayersPageParser:

    def __init__(self, players_page_text):
        self._soup = BeautifulSoup(players_page_text, SOUP_HTML_PARSER)
        self._players = []

    def get_players_ref_list(self):
        if not self._players:
            players_table = self._soup.find_all(A_TAG, class_=A_PLAYERS_LIST)
            for player_a_tag in players_table:
                self._players.append(PlayerRefFactory.create_from_a_tag(player_a_tag))
        return self._players


class PlayerRefFactory:
    @classmethod
    def create_from_a_tag(cls, a_tag):
        return PlayerRef(a_tag.attrs['href'])


class PlayerRef:

    def __init__(self, href):
        self.href = FUTWIZ_BASE_URL + href
        self.page_source = None

    def get_dict(self):
        LAST_ELEMENT = -1
        return {
            GeneralPlayerData.ID: self.href.split('/')[LAST_ELEMENT],
            GeneralPlayerData.FutwizLink: self.href
        }


class PlayersPageUrlGenerator:
    _URL = "https://www.futwiz.com/en/fc24/players?page={page_number}"

    def __init__(self, start_page_no):
        self._current_page = start_page_no

    def next_page(self):
        self._current_page += 1

    def get_page_url(self):
        return self._URL.format(page_number=self._current_page)

    def get_page_number(self):
        return self._current_page


class PlayersLastPage:
    _PAGE_START = 723

    def __init__(self):
        self.page_url_generator = PlayersPageUrlGenerator(self._PAGE_START)
        self.last_page_no = None
        self._number_of_players_in_page = None
        self._get_request = HttpGetRequestFactory.create(None, 3)

    def get_page_number(self):
        while _ := PlayersPageParser(
                self._get_request.get(self.page_url_generator.get_page_url())).get_players_ref_list():
            self._number_of_players_in_page = len(_)
            self.page_url_generator.next_page()
            self._get_request.get(self.page_url_generator.get_page_url())
        return self.page_url_generator.get_page_number() - 1

    def get_no_players(self):
        if self._number_of_players_in_page is None:
            self.get_page_number()
        return self._number_of_players_in_page
