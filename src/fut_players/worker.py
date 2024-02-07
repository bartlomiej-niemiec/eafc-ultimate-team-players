import time
from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.player_page.futwiz_concrete_player_page import PlayerPage


class Worker:

    @classmethod
    def work(cls, players_page_url, request_delay, logging_queue, page_complete_monitor):
        players_page = PlayersPage(players_page_url.get_next_page_url())
        players = players_page.get_players_ref_list()
        for player in players:
            player_page = PlayerPage(player.href)
            player_data = player_page.get_player_data()
            logging_queue.put(player_data)
            time.sleep(request_delay)
        page_complete_monitor.complete()
