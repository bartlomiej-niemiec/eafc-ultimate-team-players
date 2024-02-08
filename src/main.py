from fut_players.fut_players import fut_players_runner
from fut_players.csv_logger.logger import Logger
from fut_players.progress_bar.page_complete_monitor import PageCompleteMonitor
from fut_players.progress_bar.progress_bar import FutCompleteProgressBar
from fut_players.thread_safe_player_page import TSPlayersPageUrlGenerator
from fut_players.thread_safe_queue import LoggingQueue
from futwiz.utils.last_page_checker import PlayersLastPage
from futwiz.utils.constants import NO_PLAYERS_PER_PAGE
from utils.constants import DELAY_BETWEEN_REQUEST
from fut_players.worker_toolset import WorkerToolset


if __name__ == "__main__":
    start_page = 0
    end_page = 2
    futwiz_last_page = PlayersLastPage()
    no_players_in_last_page = None
    if end_page != futwiz_last_page.get_last_page_number():
        no_players_in_last_page = NO_PLAYERS_PER_PAGE
    else:
        no_players_in_last_page = futwiz_last_page.get_number_of_players()
    progress_bar = FutCompleteProgressBar(start_page_no=start_page, end_page_no=end_page, no_players_in_last_page=no_players_in_last_page)
    page_complete_monitor = PageCompleteMonitor()
    page_complete_monitor.RegisterObserver(progress_bar)
    player_page_generator = TSPlayersPageUrlGenerator(start_page)
    logging_queue = LoggingQueue()
    worker_toolset = WorkerToolset(
        logging_queue,
        page_complete_monitor,
        player_page_generator,
        DELAY_BETWEEN_REQUEST
    )
    logger = Logger(worker_toolset.logging_queue)
    logger.start()
    fut_players_runner(worker_toolset, end_page)
    logger.stop()
