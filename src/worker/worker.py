import time
from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.player_page.futwiz_concrete_player_page import PlayerPage
from utils.constants import DELAY_BETWEEN_REQUEST


class Worker:

    @classmethod
    def dig(cls, players_page_url):
        players_page = PlayersPage(players_page_url.get_next_page_url())
        players = players_page.get_players_ref_list()
        i = 0
        for player in players:
            player_page = PlayerPage(player.href)
            player_data = player_page.get_player_data()
            print(f"No: {i + 1}: {player_data}")
            i += 1
            time.sleep(DELAY_BETWEEN_REQUEST)
