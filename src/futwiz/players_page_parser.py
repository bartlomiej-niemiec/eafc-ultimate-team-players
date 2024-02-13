from bs4 import BeautifulSoup
from futwiz.constants import FUTWIZ_BASE_URL, A_PLAYERS_LIST
from utils.constants import SOUP_HTML_PARSER, A_TAG


class PlayersPageParser:

    def __init__(self, players_page_text):
        self._soup = BeautifulSoup(players_page_text, SOUP_HTML_PARSER)
        self._players = []

    def get_players_ref_list(self):
        self._build_players_list()
        return self._players

    def _build_players_list(self):
        if not self._players:
            players_table = self._soup.find_all(A_TAG, class_=A_PLAYERS_LIST)
            for element in players_table:
                self._players.append(create_player_ref(element))


class PlayerRef:

    def __init__(self, href):
        self.href = FUTWIZ_BASE_URL + href
        self._page_source = None

    def set_page_source(self, context):
        self._page_source = context

    def get_page_source(self):
        return self._page_source


def create_player_ref(a_tag):
    return PlayerRef(a_tag.attrs['href'])