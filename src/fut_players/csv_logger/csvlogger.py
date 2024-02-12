import time
from threading import Thread, Event
from fut_players.csv_logger.player_data_parser import PlayerDataParser
import csv

LOGGER_THREAD_DELAY = 0.2
FILES_NAME = 'fut_players.csv'


class CsvLogger(Thread):

    def __init__(self, shared_queue, player_complete_notifier):
        super(CsvLogger, self).__init__()
        self.shared_queue = shared_queue
        self._stop_event = Event()
        self._csv_dictwriter = None
        self._player_complete_notifier = player_complete_notifier
        self._main_loop_in_progress = False

    def run(self):
        self._logger()

    def stop(self):
        self._stop_event.set()

    def _logger(self):
        queue_object = None
        init_csv_logger = True
        with open(FILES_NAME, 'w', newline='', encoding="utf-8") as csvfile:
            while True:
                if self._stop_event.isSet():
                    self._write_queue_lefts_and_terminate()
                    break
                if not self.shared_queue.empty():
                    queue_object = self.shared_queue.get()
                    player_data = PlayerDataParser(queue_object).parse_and_get_player_data()
                    if init_csv_logger:
                        self._create_csv_dict_write(csvfile, player_data.keys())
                        self._wirte_headers()
                        init_csv_logger = False
                    self._csv_dictwriter.writerow(player_data)
                    self._player_complete_notifier.increment()
                time.sleep(LOGGER_THREAD_DELAY)

    def _create_csv_dict_write(self, csvfile, headers):
        self._csv_dictwriter = csv.DictWriter(csvfile, fieldnames=headers)

    def _wirte_headers(self):
        self._csv_dictwriter.writeheader()

    def _write_queue_lefts_and_terminate(self):
        while not self.shared_queue.empty():
            queue_object = self.shared_queue.get()
            player_data = PlayerDataParser(queue_object).parse_and_get_player_data()
            self._csv_dictwriter.writerow(player_data)
            self._player_complete_notifier.increment()