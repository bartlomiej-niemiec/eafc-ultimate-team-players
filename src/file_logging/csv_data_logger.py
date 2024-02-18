import config
import csv
from futwiz.player_page.player_data_template import PlayerDataTemplateFactory
from futwiz.player_page.player_page_parser import PlayerDataParser
import time
from threading import Thread, Event

LOGGER_THREAD_DELAY = config.LOGGING_THREAD_DELAY_S
FILES_NAME = config.CSV_FILE_NAME


class CsvLogger(Thread):

    def __init__(self, player_ref_queue, player_complete_notifier):
        super(CsvLogger, self).__init__()
        self.player_ref_queue = player_ref_queue
        self._stop_event = Event()
        self._csv_dictwriter = None
        self._player_complete_notifier = player_complete_notifier
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
                    self._write_player_to_csv_and_update_progressbar(self.player_ref_queue.get())
                time.sleep(LOGGER_THREAD_DELAY)

    def _init_csv_writer(self, csvfile):
        headers = PlayerDataTemplateFactory().create(config.INCLUDE_PLAYER_STATS).keys()
        self._csv_dictwriter = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
        self._csv_dictwriter.writeheader()

    def _write_queue_lefts_and_terminate(self):
        while not self.player_ref_queue.empty():
            self._write_player_to_csv_and_update_progressbar(self.player_ref_queue.get())

    def _write_player_to_csv_and_update_progressbar(self, player_ref):
        player_data = self._player_data_parser.parse_and_get_player_data(
            player_ref.page_source,
            config.INCLUDE_PLAYER_STATS
        )
        player_data.update(player_ref.get_dict())
        self._csv_dictwriter.writerow(player_data)
        self._player_complete_notifier.complete()