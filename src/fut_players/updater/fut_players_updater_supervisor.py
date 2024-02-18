from fut_players.common.page_visitor import PageVisitorWithStopEvent
from threading import Thread, Event


class FutPlayersUpdaterSupervisor:

    def __init__(self, no_more_to_update: Event, toolset):
        super(FutPlayersUpdaterSupervisor, self).__init__()
        self._no_more_to_update = no_more_to_update
        self._stop_event = Event()
        self._toolset = toolset

    def start(self):
        while not self._no_more_to_update.is_set() and not self._stop_event.is_set():
            thread = Thread(target = PageVisitorWithStopEvent.work, args = (self._toolset, self._no_more_to_update))
            thread.start()
            thread.join()

    def stop(self):
        self._stop_event.set()
