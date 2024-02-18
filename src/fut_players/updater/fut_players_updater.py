from threading import Event

from fut_players.common.page_visitor import Toolset
from fut_players.updater.fut_players_updater_supervisor import FutPlayersUpdaterSupervisor
from file_logging.csv_data_updater import CsvUpdater
from futwiz.players_page.players_page_url_generator import PlayerPageUrlFactory
from futwiz.players_page.util import PlayersPageType
from progress_bar.players_complete_progressbar import PlayersCompleteProgressBar
from progress_bar.player_save_notifier import PlayerSaveNotifier
from utils.get_requests.get_request_factory import HttpGetRequestFactory
from utils.thread_safe_queue import ThreadSafeQueue

PROGRESS_BAR_FORMAT = "[players added: {n_fmt} time spent: {elapsed}]"


class FutPlayersUpdater:

    def __init__(self, config):
        self._logging_queue = ThreadSafeQueue()
        self._config = config
        self._supervisor = None
        self._no_more_to_update = Event()
        self._progress_bar = None
        self._player_save_notifier = None
        self._logging_thread = None
        self._toolset = None

    def __del__(self):
        print("Update Complete!")

    def run(self):
        self._init()
        self._spawn_logging_thread()
        self._logging_thread.start()
        self._supervisor.start()
        self._logging_thread.join()

    def _spawn_logging_thread(self):
        self._logging_thread = CsvUpdater(
            self._logging_queue,
            self._config.CSV_FILE_NAME,
            self._no_more_to_update,
            self._player_save_notifier,
            self._config.DELAY_TO_NEXT_REQUEST_S
        )

    def _init(self):
        self._init_progressbar()
        self._init_player_progress_notification()
        self._appoint_supervisor()

    def _init_progressbar(self):
        self._progress_bar = PlayersCompleteProgressBar(None, PROGRESS_BAR_FORMAT)

    def _init_player_progress_notification(self):
        self._player_save_notifier = PlayerSaveNotifier()
        self._player_save_notifier.register_observer(self._progress_bar)

    def _appoint_supervisor(self):
        self._toolset = Toolset(
            self._logging_queue,
            PlayerPageUrlFactory.create(0, PlayersPageType.LatestAddedPlayers),
            self._config.DELAY_TO_NEXT_REQUEST_S,
            HttpGetRequestFactory.create(None, self._config.MAX_RETRIES),
            PlayersPageType.LatestAddedPlayers
        )
        self._supervisor = FutPlayersUpdaterSupervisor(
            self._no_more_to_update,
            self._toolset
        )
