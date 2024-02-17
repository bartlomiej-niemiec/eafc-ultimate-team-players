from threading import Event
from fut_players.updater.fut_players_updater_supervisor import FutPlayersUpdaterSupervisor
from file_logging.csv_data_updater import CsvUpdater
from progress_bar.base_progress_bar import BaseProgressBar
from progress_bar.player_save_notifier import PlayerSaveNotifier
from utils.thread_safe_queue import ThreadSafeQueue
import config


class FutPlayersUpdater:

    def __init__(self):
        self._logging_queue = ThreadSafeQueue()
        self._supervisor = None
        self._no_more_to_update = Event()
        self._progress_bar = BaseProgressBar()
        self._player_save_notifier = PlayerSaveNotifier()
        self._player_save_notifier.register_observer(self._progress_bar)

    def __del__(self):
        print("Update Complete!")

    def run(self):
        self._appoint_supervisor()
        logger = CsvUpdater(self._logging_queue, config.CSV_FILE_NAME, self._no_more_to_update, self._player_save_notifier)
        logger.start()
        self._supervisor.start()
        logger.join()

    def _appoint_supervisor(self):
        self._supervisor = FutPlayersUpdaterSupervisor(
            self._logging_queue,
            self._no_more_to_update
        )
