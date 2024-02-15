from fut_players.worker import Supervisor
from csv_logger.csv_data_logger import CsvLogger
from progress_bar.player_save_notifier import PlayerSaveNotifier
from progress_bar.progress_bar import FutCompleteProgressBar
from utils.thread_safe_queue import ThreadSafeQueue
from futwiz.players_page import PlayersLastPage
from futwiz.constants import NO_PLAYERS_PER_PAGE


class FutPlayers:

    def __init__(self, start_page_number=0, last_page_number=None):
        self.last_page_number = last_page_number
        self.start_page_number = start_page_number
        self._logging_queue = ThreadSafeQueue()
        self._no_players_in_last_page = None
        self._progress_bar = None
        self._player_save_notifier = None
        self._supervisor = None

    def run(self):
        self._init()
        logger = CsvLogger(self._logging_queue, self._player_save_notifier)
        logger.start()
        self._supervisor.start()
        logger.stop()

    def _init(self):
        self._get_last_players_page()
        self._init_progress_bar()
        self._init_player_progress_notification()
        self._appoint_supervisor()

    def _get_last_players_page(self):
        futwiz_last_page = PlayersLastPage()
        futwiz_last_page_number = futwiz_last_page.get_page_number()
        if self.last_page_number:
            if self.last_page_number != futwiz_last_page_number:
                self._no_players_in_last_page = NO_PLAYERS_PER_PAGE
            else:
                self._no_players_in_last_page = futwiz_last_page.get_no_players()
        else:
            self.last_page_number = futwiz_last_page_number
            self._no_players_in_last_page = futwiz_last_page.get_no_players()

    def _init_progress_bar(self):
        self._progress_bar = FutCompleteProgressBar(start_page_no=self.start_page_number,
                                                    end_page_no=self.last_page_number,
                                                    no_players_in_last_page=self._no_players_in_last_page)

    def _init_player_progress_notification(self):
        self._player_save_notifier = PlayerSaveNotifier()
        self._player_save_notifier.register_observer(self._progress_bar)

    def _appoint_supervisor(self):
        self._supervisor = Supervisor(
            self._logging_queue,
            self.start_page_number,
            self.last_page_number
        )


