from ut_players.all_players_mode.utp_all_players_csv_logger import AllPlayersLogger
from ut_players.common.page_visitor import Toolset
from ut_players.all_players_mode.utp_get_all_players_supervisor import UtpGetAllPlayerSupervisor
from futwiz.players_page.last_players_page import LastPlayersPage
from futwiz.constants import NO_PLAYERS_PER_PAGE

from progress_bar.players_complete_progressbar import PlayersCompleteProgressBar
from ut_players.common.utp_base import UtpBase
from utils.thread_safe_queue import ThreadSafeQueue
from futwiz.players_page.players_page_url_generator import PlayerPageUrlFactory
from futwiz.players_page.util import PlayersPageType
from utils.get_requests.get_request_factory import HttpGetRequestFactory
from utils.proxy_servers import get_proxy_servers_from_file, ProxyPool


class UtpGetAllPlayers(UtpBase):

    def __init__(self, config):
        super().__init__(config)
        self.start_page_number = config.START_PAGE
        self.last_page_number = config.END_PAGE
        self._logging_queue = ThreadSafeQueue()
        self._no_players_in_last_page = None
        self._logging_thread = None
        self._toolset = None
        self._proxy_pool = None
        self._supervisor = None

    def run(self):
        self._init()
        self._spawn_logging_thread()
        self._logging_thread.start()
        self._supervisor.start()
        self._logging_thread.stop()

    def _init(self):
        self._get_last_players_page()
        total_iterations = PlayersCompleteProgressBar.calculate_no_players_to_save(
            self.start_page_number,
            self.last_page_number,
            self._no_players_in_last_page
        )
        self._init_progress_bar(total_iterations)
        self._init_player_progress_notification()
        self._appoint_supervisor()

    def _spawn_logging_thread(self):
        self._logging_thread = AllPlayersLogger(
            self._logging_queue,
            self._player_save_notifier,
            self._config.CSV_FILEPATH,
            self._config.LOGGING_THREAD_DELAY_S,
            self._config.INCLUDE_PLAYER_STATS
        )

    def _get_last_players_page(self):
        futwiz_last_page = LastPlayersPage()
        futwiz_last_page_number = futwiz_last_page.get_page_number()
        self._no_players_in_last_page = futwiz_last_page.get_no_players()
        if self.last_page_number:
            if self.last_page_number != futwiz_last_page_number:
                self._no_players_in_last_page = NO_PLAYERS_PER_PAGE
        else:
            self.last_page_number = futwiz_last_page_number

    def _appoint_supervisor(self):
        if self._config.USE_PROXY:
            self._proxy_pool = ProxyPool(get_proxy_servers_from_file(self._config.PROXY_SERVERS_FILEPATH))
        self._toolset = Toolset(
            self._logging_queue,
            PlayerPageUrlFactory.create(self.start_page_number, PlayersPageType.AllPlayers),
            self._config.DELAY_TO_NEXT_REQUEST_S,
            HttpGetRequestFactory.create(self._proxy_pool, self._config.MAX_RETRIES),
            PlayersPageType.AllPlayers
        )
        self._supervisor = UtpGetAllPlayerSupervisor(
            self.last_page_number - self.start_page_number + 1,
            self._config.NO_WORKING_THREADS,
            self._toolset
        )
