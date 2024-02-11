from fut_players.worker.worker import start_work
from utils.proxy_pool import ProxyPool
from utils.proxy_servers import HTTP_PROXIES, get_from_file
from fut_players.csv_logger.csvlogger import CsvLogger
from fut_players.progress_bar.page_complete_notifier import PlayerCompleteNotifier
from fut_players.progress_bar.progress_bar import FutCompleteProgressBar
from fut_players.csv_logger.thread_safe_queue import ThreadSafeQueue
from futwiz.players_page.futwiz_players_page_url import PlayersPageUrlGenerator
from futwiz.utils.last_page_checker import PlayersLastPage
from futwiz.utils.constants import NO_PLAYERS_PER_PAGE
from utils.constants import DELAY_BETWEEN_REQUEST
from fut_players.worker.worker_toolset import WorkerToolset


class FutPlayers:

    def __init__(self, start_page_number=0, last_page_number=None):
        self.last_page_number = last_page_number
        self.start_page_number = start_page_number
        self._no_players_in_last_page = None
        self._progress_bar = None
        self._page_complete_notifier = None
        self._player_page_generator = None
        self._logging_queue = None
        self._proxies = None

    def run(self):
        self._init()
        logger = CsvLogger(self._logging_queue)
        logger.start()
        start_work(self.worker_toolset, self.last_page_number - self.start_page_number + 1)
        logger.stop()

    def _init(self):
        self._get_last_players_page()
        self._build_the_toolset()

    def _get_last_players_page(self):
        futwiz_last_page = PlayersLastPage()
        futwiz_last_page_number = futwiz_last_page.get_last_page_number()
        if self.last_page_number:
            if self.last_page_number != futwiz_last_page_number:
                self._no_players_in_last_page = NO_PLAYERS_PER_PAGE
            else:
                self._no_players_in_last_page = futwiz_last_page.get_number_of_players()
        else:
            self.last_page_number = futwiz_last_page_number
            self._no_players_in_last_page = futwiz_last_page.get_number_of_players()

    def _build_the_toolset(self):
        self._progress_bar = FutCompleteProgressBar(start_page_no=self.start_page_number, end_page_no=self.last_page_number,
                                                    no_players_in_last_page=self._no_players_in_last_page)
        self._page_complete_notifier = PlayerCompleteNotifier()
        self._page_complete_notifier.register_observer(self._progress_bar)
        self._player_page_generator = PlayersPageUrlGenerator(self.start_page_number)
        self._logging_queue = ThreadSafeQueue()
        self._proxies = ProxyPool(get_from_file(r"C:\Users\bniem\Downloads\free_proxy_servers.txt"))
        self.worker_toolset = WorkerToolset(
            self._logging_queue,
            self._page_complete_notifier,
            self._player_page_generator,
            self._proxies,
            DELAY_BETWEEN_REQUEST
        )

