from bs4 import BeautifulSoup
from futwiz.players_page.util import PlayersPageType
from futwiz.players_page.constants import A_PLAYERS_LIST, A_LATEST_PLAYERS_LIST
from futwiz.players_page.player_ref import PlayerRefFactory
from utils.constants import SOUP_HTML_PARSER, A_TAG


class PlayerPageParserFactory:

    @classmethod
    def create(cls, page_source, page_type):
        if page_type == PlayersPageType.AllPlayers:
            return PlayersPageParser(page_source, A_PLAYERS_LIST)
        elif page_type == PlayersPageType.LatestAddedPlayers:
            return PlayersPageParser(page_source, A_LATEST_PLAYERS_LIST)


class PlayersPageParser:

    def __init__(self, players_page_text, a_tag_class):
        self._soup = BeautifulSoup(players_page_text, SOUP_HTML_PARSER)
        self._players = []
        self._a_tag_class = a_tag_class

    def get_players_ref_list(self):
        if not self._players:
            players_table = self._soup.find_all(A_TAG, class_=self._a_tag_class)
            self._players = [PlayerRefFactory.create(player_a_tag) for player_a_tag in players_table]
        return self._players
