import time

from file_logging.utils import does_file_include_player_stats, get_csv_content
from fut_players.price_update.fur_players_price_update_supervisor import FutPlayersPriceUpdaterSupervisor
from fut_players.price_update.player_url_generator import PlayerUrlGenerator
from progress_bar.player_save_notifier import PlayerSaveNotifier
from progress_bar.players_complete_progressbar import PlayersCompleteProgressBar
from utils.get_requests.get_request_factory import HttpGetRequestFactory
from utils.proxy_servers import ProxyPool, get_proxy_servers_from_file
from utils.thread_safe_queue import ThreadSafeQueue
from fut_players.common.player_visitor import PlayerVisitorToolset
from file_logging.csv_price_updater import CsvpPriceUpdater

TERMINATE_DELAY = 2


class FutPlayersPriceUpdater:

    def __init__(self, config):
        self._logging_queue = ThreadSafeQueue()
        self._progress_bar = None
        self._player_save_notifier = None
        self._supervisor = None
        self._logging_thread = None
        self._toolset = None
        self._proxy_pool = None
        self._config = config
        self._player_stats_in_file = does_file_include_player_stats(config.CSV_FILE_NAME)
        self._csv_content = get_csv_content(config.CSV_FILE_NAME)
        self._player_getter = PlayerUrlGenerator(self._csv_content)

    def run(self):
        self._init()
        self._logging_thread.start()
        self._supervisor.start()
        self._supervisor.join()
        self._logging_thread.stop()
        time.sleep(TERMINATE_DELAY)

    def stop(self):
        pass

    def _init(self):
        self._init_progress_bar()
        self._init_player_progress_notification()
        self._appoint_supervisor()
        self._spawn_logging_thread()

    def _spawn_logging_thread(self):
        self._logging_thread = CsvpPriceUpdater(
            self._logging_queue,
            self._config.CSV_FILE_NAME,
            self._player_save_notifier,
            self._config.DELAY_TO_NEXT_REQUEST_S
        )

    def _init_progress_bar(self):
        self._progress_bar = PlayersCompleteProgressBar(len(self._csv_content) - 1)

    def _init_player_progress_notification(self):
        self._player_save_notifier = PlayerSaveNotifier()
        self._player_save_notifier.register_observer(self._progress_bar)

    def _appoint_supervisor(self):
        if self._config.USE_PROXY:
            self._proxy_pool = ProxyPool(get_proxy_servers_from_file(self._config.PROXY_SERVERS_FILE_PATH))
        self._toolset = PlayerVisitorToolset(
            self._logging_queue,
            HttpGetRequestFactory.create(self._proxy_pool, self._config.MAX_RETRIES),
            self._player_getter
        )
        self._supervisor = FutPlayersPriceUpdaterSupervisor(
            self._config.NO_WORKING_THREADS,
            self._toolset
        )
