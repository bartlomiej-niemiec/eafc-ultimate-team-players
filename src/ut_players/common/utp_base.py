from abc import ABC, abstractmethod
from progress_bar.player_save_notifier import PlayerSaveNotifier
from progress_bar.players_complete_progressbar import PlayersCompleteProgressBar


class UtpBase(ABC):

    def __init__(self, config):
        self._config = config
        self._progress_bar = None
        self._player_save_notifier = None
        self._supervisor = None

    @abstractmethod
    def run(self):
        pass

    def _init_progress_bar(self, total_iterations):
        self._progress_bar = PlayersCompleteProgressBar(total_iterations)

    def _init_player_progress_notification(self):
        self._player_save_notifier = PlayerSaveNotifier()
        self._player_save_notifier.register_observer(self._progress_bar)

    @abstractmethod
    def _appoint_supervisor(self):
        pass

