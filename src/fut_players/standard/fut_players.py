from file_logging.csv_data_logger import CsvLogger
from fut_players.standard.fut_players_supervisor import FutPlayersSupervisor
from futwiz.players_page.last_players_page import LastPlayersPage
from futwiz.constants import NO_PLAYERS_PER_PAGE

from progress_bar.player_save_notifier import PlayerSaveNotifier
from progress_bar.players_complete_progressbar import PlayersCompleteProgressBar
from utils.thread_safe_queue import ThreadSafeQueue


class FutPlayers:

    def __init__(self, start_page_number=0, last_page_number=None):
        self.last_page_number = last_page_number
        self.start_page_number = start_page_number
        self._logging_queue = ThreadSafeQueue()
        self._no_players_in_last_page = None
        self._progress_bar = None
        self._player_save_notifier = None
        self._supervisor = None
        self._logging_thread = None

    def run(self):
        self._init()
        self._spawn_logging_thread()
        self._logging_thread.start()
        self._supervisor.start()
        self._logging_thread.stop()

    def _init(self):
        self._get_last_players_page()
        self._init_progress_bar()
        self._init_player_progress_notification()
        self._appoint_supervisor()

    def _spawn_logging_thread(self):
        self._logging_thread = CsvLogger(self._logging_queue, self._player_save_notifier)

    def _get_last_players_page(self):
        futwiz_last_page = LastPlayersPage()
        futwiz_last_page_number = futwiz_last_page.get_page_number()
        self._no_players_in_last_page = futwiz_last_page.get_no_players()
        if self.last_page_number:
            if self.last_page_number != futwiz_last_page_number:
                self._no_players_in_last_page = NO_PLAYERS_PER_PAGE
        else:
            self.last_page_number = futwiz_last_page_number

    def _init_progress_bar(self):
        total_iterations = PlayersCompleteProgressBar.calculate_no_players_to_save(
            self.start_page_number,
            self.last_page_number,
            self._no_players_in_last_page
        )
        self._progress_bar = PlayersCompleteProgressBar(total_iterations)

    def _init_player_progress_notification(self):
        self._player_save_notifier = PlayerSaveNotifier()
        self._player_save_notifier.register_observer(self._progress_bar)

    def _appoint_supervisor(self):
        self._supervisor = FutPlayersSupervisor(
            self._logging_queue,
            self.start_page_number,
            self.last_page_number
        )