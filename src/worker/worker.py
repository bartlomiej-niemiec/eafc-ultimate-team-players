import time
from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.player_page.futwiz_concrete_player_page import PlayerPage


class Worker:

    DELAY_BETWEEN_REQUEST = 2

    @classmethod
    def dig(cls, players_page_url):
        players_page = PlayersPage()
        page_url = players_page_url.get_next_page_url()
        players_page.go_page(page_url)
        players = players_page.get_players()
        for player in players:
            player_page = PlayerPage(player.href)
            player_page.fetch_data()
            player_dict = player_page.get_data()
            print(player_dict)
            time.sleep(cls.DELAY_BETWEEN_REQUEST)
