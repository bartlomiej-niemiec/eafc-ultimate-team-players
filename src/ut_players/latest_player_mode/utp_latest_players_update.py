from threading import Event

from ut_players.common.page_visitor import Toolset
from ut_players.common.utp_base import UtpBase
from ut_players.latest_player_mode.utp_latest_players_update_supervisor import UtpLatestPlayerUpdateSupervisor
from ut_players.latest_player_mode.utp_latest_players_csv_logger import LatestPlayersLogger
from futwiz.players_page.players_page_url_generator import PlayerPageUrlFactory
from futwiz.players_page.util import PlayersPageType
from utils.get_requests.get_request_factory import HttpGetRequestFactory
from utils.thread_safe_queue import ThreadSafeQueue

PROGRESS_BAR_FORMAT = "[players added: {n_fmt} time spent: {elapsed}]"


class UtpLatestPlayersUpdate(UtpBase):

    def __init__(self, config):
        super().__init__(config)
        self._logging_queue = ThreadSafeQueue()
        self._no_more_to_update = Event()
        self._logging_thread = None
        self._toolset = None
        self._supervisor = None

    def __del__(self):
        print("Update Complete!")

    def run(self):
        self._init()
        self._spawn_logging_thread()
        self._logging_thread.start()
        self._supervisor.start()
        self._logging_thread.join()

    def _init(self):
        self._init_progress_bar(None)
        self._init_player_progress_notification()
        self._appoint_supervisor()

    def _spawn_logging_thread(self):
        self._logging_thread = LatestPlayersLogger(
            self._logging_queue,
            self._config.CSV_FILEPATH,
            self._no_more_to_update,
            self._player_save_notifier,
            self._config.DELAY_TO_NEXT_REQUEST_S
        )

    def _appoint_supervisor(self):
        self._toolset = Toolset(
            self._logging_queue,
            PlayerPageUrlFactory.create(0, PlayersPageType.LatestAddedPlayers),
            self._config.DELAY_TO_NEXT_REQUEST_S,
            HttpGetRequestFactory.create(None, self._config.MAX_RETRIES),
            PlayersPageType.LatestAddedPlayers
        )
        self._supervisor = UtpLatestPlayerUpdateSupervisor(
            self._no_more_to_update,
            self._toolset
        )
