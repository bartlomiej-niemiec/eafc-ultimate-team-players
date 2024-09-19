import time
from ut_players.common.utils import does_file_include_player_stats
from utils.csv_utils import get_csv_content
from ut_players.common.utp_base import UtpBase
from ut_players.price_update_mode.utp_price_update_supervisor import FutPlayersPriceUpdaterSupervisor
from ut_players.common.player_url_generator import PlayerUrlGenerator
from utils.get_requests.get_request_factory import HttpGetRequestFactory
from utils.proxy_servers import ProxyPool, get_proxy_servers_from_file
from utils.thread_safe_queue import ThreadSafeQueue
from ut_players.common.player_visitor import PlayerVisitorToolset
from ut_players.price_update_mode.utp_price_update_csv_logger import PriceUpdateLogger

TERMINATE_DELAY = 2


class FutPlayersPriceUpdater(UtpBase):

    def __init__(self, config):
        super().__init__(config)
        self._logging_queue = ThreadSafeQueue()
        self._logging_thread = None
        self._toolset = None
        self._proxy_pool = None
        self._config = config
        self._player_stats_in_file = does_file_include_player_stats(config.CSV_FILEPATH)
        self._csv_content = get_csv_content(config.CSV_FILEPATH)
        self._player_getter = PlayerUrlGenerator(self._csv_content)
        self._supervisor = None

    def run(self):
        self._init()
        self._logging_thread.start()
        self._supervisor.start()
        self._supervisor.join()
        self._logging_thread.stop()
        time.sleep(TERMINATE_DELAY)

    def _init(self):
        self._init_progress_bar(len(self._csv_content) - 1)
        self._init_player_progress_notification()
        self._appoint_supervisor()
        self._spawn_logging_thread()

    def _spawn_logging_thread(self):
        self._logging_thread = PriceUpdateLogger(
            self._logging_queue,
            self._config.CSV_FILEPATH,
            self._player_save_notifier,
            self._config.DELAY_TO_NEXT_REQUEST_S,
            self._config.EA_FC_VERSION
        )

    def _appoint_supervisor(self):
        if self._config.USE_PROXY:
            self._proxy_pool = ProxyPool(get_proxy_servers_from_file(self._config.PROXY_SERVERS_FILEPATH))
        self._toolset = PlayerVisitorToolset(
            self._logging_queue,
            HttpGetRequestFactory.create(self._proxy_pool, self._config.MAX_RETRIES),
            self._player_getter
        )
        self._supervisor = FutPlayersPriceUpdaterSupervisor(
            self._config.NO_WORKING_THREADS,
            self._toolset
        )
