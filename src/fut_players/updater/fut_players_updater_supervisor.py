import time

from fut_players.common.page_visitor import Toolset, PageVisitor
from futwiz.players_page.players_page_url_generator import PlayerPageUrlFactory
from futwiz.players_page.util import PlayersPageType
from threading import Thread, Event


class FutPlayersUpdaterSupervisor(Thread):

    def __init__(self, csv_logging_queue, no_more_to_update: Event):
        super(FutPlayersUpdaterSupervisor, self).__init__()
        self._worker_toolset = Toolset(
            csv_logging_queue,
            PlayerPageUrlFactory.create(None, PlayersPageType.LatestAddedPlayers),
        )
        self._no_more_to_update = no_more_to_update
        self._stop_event = Event()

    def run(self):
        while not self._no_more_to_update.is_set() and not self._stop_event.is_set():
            PageVisitor.work(self._worker_toolset)
            time.sleep(1)

    def stop(self):
        self._stop_event.set()
