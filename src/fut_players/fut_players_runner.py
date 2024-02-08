from fut_players.worker.fut_players import start_work
from fut_players.csv_logger.logger import Logger
from fut_players.progress_bar.page_complete_monitor import PageCompleteMonitor
from fut_players.progress_bar.progress_bar import FutCompleteProgressBar
from fut_players.worker.thread_safe_player_page import TSPlayersPageUrlGenerator
from fut_players.csv_logger.csv_logging_queue import LoggingQueue
from futwiz.utils.last_page_checker import PlayersLastPage
from futwiz.utils.constants import NO_PLAYERS_PER_PAGE
from utils.constants import DELAY_BETWEEN_REQUEST
from fut_players.worker.worker_toolset import WorkerToolset


class FutPlayers:

    def __init__(self, start_page=0, last_page=None):
        self.last_page = last_page
        self.start_page = start_page
        self._no_players_in_last_page = None
        self._progress_bar = None
        self._page_complete_monitor = None
        self._player_page_generator = None

    def run(self):
        self._init()
        logger = Logger(self.worker_toolset.logging_queue)
        logger.start()
        start_work(self.worker_toolset, self.last_page)
        logger.stop()

    def _init(self):
        self._get_last_page_to_work()
        self._build_the_toolset()

    def _get_last_page_to_work(self):
        futwiz_last_page = PlayersLastPage()
        futwiz_last_page_number = futwiz_last_page.get_last_page_number()
        if self.last_page:
            if self.last_page != futwiz_last_page_number:
                self._no_players_in_last_page = NO_PLAYERS_PER_PAGE
            else:
                self._no_players_in_last_page = futwiz_last_page.get_number_of_players()
        else:
            self.last_page = futwiz_last_page_number
            self._no_players_in_last_page = futwiz_last_page.get_number_of_players()

    def _build_the_toolset(self):
        self._progress_bar = FutCompleteProgressBar(start_page_no=self.start_page, end_page_no=self.last_page,
                                                    no_players_in_last_page=self._no_players_in_last_page)
        self._page_complete_monitor = PageCompleteMonitor()
        self._page_complete_monitor.RegisterObserver(self._progress_bar)
        self._player_page_generator = TSPlayersPageUrlGenerator(self.start_page)
        logging_queue = LoggingQueue()
        self.worker_toolset = WorkerToolset(
            logging_queue,
            self._page_complete_monitor,
            self._player_page_generator,
            DELAY_BETWEEN_REQUEST
        )

