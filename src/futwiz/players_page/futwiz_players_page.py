from bs4 import BeautifulSoup
from futwiz.utils.constants import FUTWIZ_BASE_URL, A_PLAYERS_LIST
from utils.constants import SOUP_HTML_PARSER_FEATURE, A_TAG
import requests


class PlayersPage:

    def __init__(self):
        self._players_retriever = PlayersOnPlayersPage()
        self.source = None

    def go_page(self, page_url):
        self.source = requests.get(page_url).text

    def get_players(self):
        self._players_retriever.set_page_source(self.source)
        self._players_retriever.build_players_list()
        return self._players_retriever.get_players_ref_list()


class PlayersOnPlayersPage:

    def __init__(self):
        self._soup = None
        self._players = []

    def set_page_source(self, page_source):
        self._soup = BeautifulSoup(page_source, SOUP_HTML_PARSER_FEATURE)
        self._players = []

    def build_players_list(self):
        if not self._players:
            players_table = self._soup.find_all(A_TAG, class_=A_PLAYERS_LIST)
            for element in players_table:
                self._players.append(create_player_ref(element))

    def get_players_ref_list(self):
        return self._players


class PlayerRef:

    def __init__(self, href):
        self.href = FUTWIZ_BASE_URL + href


def create_player_ref(a_tag):
    return PlayerRef(a_tag.attrs['href'])
