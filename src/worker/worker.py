import time
from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.player_page.futwiz_concrete_player_page import PlayerPage
from utils.constants import DELAY_BETWEEN_REQUEST


class Worker:

    @classmethod
    def dig(cls, players_page_url):
        players_page = PlayersPage()
        page_url = players_page_url.get_next_page_url()
        players_page.go_page(page_url)
        players = players_page.get_players()
        i = 0
        for player in players:
            player_page = PlayerPage(player.href)
            player_page.fetch_data()
            player_dict = player_page.get_data()
            print(f"No: {i + 1}: {player_dict}")
            i += 1
            time.sleep(DELAY_BETWEEN_REQUEST)
