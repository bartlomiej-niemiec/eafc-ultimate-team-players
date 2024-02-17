from threading import Event
from fut_players.updater.fut_players_updater_supervisor import FutPlayersUpdaterSupervisor
from file_logging.csv_data_updater import CsvUpdater
from utils.thread_safe_queue import ThreadSafeQueue
import config


class FutPlayersUpdater:

    def __init__(self):
        self._logging_queue = ThreadSafeQueue()
        self._supervisor = None
        self._no_more_to_update = Event()

    def run(self):
        self._appoint_supervisor()
        logger = CsvUpdater(self._logging_queue, config.CSV_FILE_NAME, self._no_more_to_update)
        logger.start()
        self._supervisor.start()
        logger.join()
        self._supervisor.join()
        print("Update Complete!")

    def _appoint_supervisor(self):
        self._supervisor = FutPlayersUpdaterSupervisor(
            self._logging_queue,
            self._no_more_to_update
        )
