import time
from threading import Thread, Event
from fut_players.csv_logger.player_data_parser import PlayerDataParser
import csv

LOGGER_THREAD_DELAY = 0.2
ALT_POS_KEY = 'Alt Pos.'
FILES_NAME = 'fut_players.csv'

GK_HEADERS = [
    "DIV",
    "GK. Diving",
    "HAN",
    "GK. Handling",
    "KIC",
    "GK. Kicking",
    "SPD",
    "POS",
    "GK. Pos",
    "REF",
    "GK. Reflexes",
]


class CsvLogger(Thread):

    def __init__(self, shared_queue):
        super(CsvLogger, self).__init__()
        self.shared_queue = shared_queue
        self._stop_event = Event()
        self._csv_dictwriter = None

    def run(self):
        self._logger()

    def stop(self):
        self._stop_event.set()
        while not self.shared_queue.empty():
            queue_object = self.shared_queue.get()
            player_data = PlayerDataParser(queue_object).parse_and_get_player_data()
            self._csv_dictwriter.writerow(player_data)

    def _logger(self):
        queue_object = None
        is_first_log = True
        with open(FILES_NAME, 'w', newline='', encoding="utf-8") as csvfile:
            while True:
                if self._stop_event.isSet():
                    break
                if not self.shared_queue.empty():
                    queue_object = self.shared_queue.get()
                    player_data = PlayerDataParser(queue_object).parse_and_get_player_data()
                    if is_first_log:
                        self._write_headers(csvfile, player_data.keys())
                        is_first_log = False
                    self._csv_dictwriter.writerow(player_data)
                time.sleep(LOGGER_THREAD_DELAY)

    def _write_headers(self, csvfile, headers):
        merged_headers = list(headers)  # + GK_HEADERS
        self._csv_dictwriter = csv.DictWriter(csvfile, fieldnames=merged_headers)
        self._csv_dictwriter.writeheader()
