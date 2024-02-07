from fut_players.fut_players import fut_players_runner
from fut_players.logger import Logger, FutCompleteProgressBar, PageCompleteMonitor
from fut_players.thread_safe_player_page import TSPlayersPageUrlGenerator
from fut_players.thread_safe_queue import LoggingQueue
from utils.constants import DELAY_BETWEEN_REQUEST


if __name__ == "__main__":
    pages = 2
    page_complete_monitor = PageCompleteMonitor()
    progress_bar = FutCompleteProgressBar(start_page_no=0, end_page_no=pages)
    page_complete_monitor.RegisterObserver(progress_bar)
    player_page_generator = TSPlayersPageUrlGenerator(0)
    logging_queue = LoggingQueue()
    logger = Logger(logging_queue)
    logger.start()
    fut_players_runner(
        player_page_generator,
        DELAY_BETWEEN_REQUEST,
        pages,
        logging_queue,
        page_complete_monitor
    )
    logger.stop()


