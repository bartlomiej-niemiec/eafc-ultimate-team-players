import time
from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.player_page.futwiz_concrete_player_page import PlayerPage
from fut_players.worker.worker_toolset import WorkerToolset


class Worker:

    @classmethod
    def work(cls, toolset: WorkerToolset):
        page_url = toolset.get_next_page_url()
        players_page = PlayersPage(page_url)
        players = players_page.get_players_ref_list()
        for player in players:
            player_page = PlayerPage(player.href)
            player_data = player_page.get_player_data()
            toolset.logging_queue.put(player_data)
            toolset.page_complete_monitor.complete()
            time.sleep(toolset.request_delay)