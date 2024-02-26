from ut_players.common.player_visitor import PlayerVisitor
from threading import Thread


class FutPlayersPriceUpdaterSupervisor:

    def __init__(self, no_threads, toolset):
        self._worker_toolset = toolset
        self._no_workers = no_threads
        self._threads = []

    def start(self):
        self._spawn_threads()

    def join(self):
        self._wait_for_finish()

    def _spawn_threads(self):
        for i in range(self._no_workers):
            thread = Thread(target=PlayerVisitor.visit, args=(self._worker_toolset,))
            thread.start()
            self._threads.append(thread)

    def _wait_for_finish(self):
        for thread in self._threads:
            thread.join()
