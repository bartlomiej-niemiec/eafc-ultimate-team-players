import time
from threading import Thread, Event
from futwiz.player_data_parser import PlayerDataParser, PlayerDataTemplateFactory
import config
import csv

LOGGER_THREAD_DELAY = config.LOGGING_THREAD_DELAY
FILES_NAME = config.CSV_FILE_NAME


class CsvLogger(Thread):

    def __init__(self, player_ref_queue, player_complete_notifier):
        super(CsvLogger, self).__init__()
        self.player_ref_queue = player_ref_queue
        self._stop_event = Event()
        self._csv_dictwriter = None
        self._player_complete_notifier = player_complete_notifier
        self._main_loop_in_progress = False
        self._player_data_parser = PlayerDataParser()

    def run(self):
        self._logger()

    def stop(self):
        self._stop_event.set()

    def _logger(self):
        queue_object = None
        with open(FILES_NAME, 'w', newline='', encoding="utf-8") as csvfile:
            self._init_csv_writer(csvfile)
            while True:
                if self._stop_event.isSet():
                    self._write_queue_lefts_and_terminate()
                    break
                if not self.player_ref_queue.empty():
                    player_ref = self.player_ref_queue.get()
                    player_data = self._player_data_parser.parse_and_get_player_data(
                        player_ref.page_source,
                        config.INCLUDE_PLAYER_STATS
                    )
                    player_data.update(player_ref.get_dict())
                    self._csv_dictwriter.writerow(player_data)
                    self._player_complete_notifier.complete()
                time.sleep(LOGGER_THREAD_DELAY)

    def _init_csv_writer(self, csvfile):
        headers = PlayerDataTemplateFactory().create_player_data_dict_template(config.INCLUDE_PLAYER_STATS).keys()
        self._csv_dictwriter = csv.DictWriter(csvfile, fieldnames=headers)
        self._csv_dictwriter.writeheader()

    def _write_queue_lefts_and_terminate(self):
        while not self.player_ref_queue.empty():
            player_ref = self.player_ref_queue.get()
            player_data = self._player_data_parser.parse_and_get_player_data(
                player_ref.page_source,
                config.INCLUDE_PLAYER_STATS
            )
            player_data.update(player_ref.get_dict())
            self._csv_dictwriter.writerow(player_data)
            self._player_complete_notifier.complete()