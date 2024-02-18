import csv
from futwiz.player_page.player_data_template import PlayerDataTemplateFactory
from futwiz.player_page.player_page_parser import PlayerDataParser
import time
from threading import Thread, Event


class CsvLogger(Thread):

    def __init__(self, player_ref_queue, player_complete_notifier, filepath, thread_interval_s, with_player_stats):
        super(CsvLogger, self).__init__()
        self.player_ref_queue = player_ref_queue
        self._stop_event = Event()
        self._csv_dictwriter = None
        self._player_complete_notifier = player_complete_notifier
        self._player_data_parser = PlayerDataParser()
        self._filepath = filepath
        self._thread_interval_s = thread_interval_s
        self._with_player_stats = with_player_stats

    def run(self):
        self._logger()

    def stop(self):
        self._stop_event.set()

    def _logger(self):
        queue_object = None
        with open(self._filepath, 'w', newline='', encoding="utf-8") as csvfile:
            self._init_csv_writer(csvfile)
            while True:
                if self._stop_event.isSet():
                    self._write_queue_lefts_and_terminate()
                    break
                if not self.player_ref_queue.empty():
                    self._write_player_to_csv_and_update_progressbar(self.player_ref_queue.get())
                time.sleep(self._thread_interval_s)

    def _init_csv_writer(self, csvfile):
        headers = PlayerDataTemplateFactory().create(self._with_player_stats).keys()
        self._csv_dictwriter = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
        self._csv_dictwriter.writeheader()

    def _write_queue_lefts_and_terminate(self):
        while not self.player_ref_queue.empty():
            self._write_player_to_csv_and_update_progressbar(self.player_ref_queue.get())

    def _write_player_to_csv_and_update_progressbar(self, player_ref):
        player_data = self._player_data_parser.parse_and_get_player_data(
            player_ref.page_source,
            self._with_player_stats
        )
        player_data.update(player_ref.get_dict())
        self._csv_dictwriter.writerow(player_data)
        self._player_complete_notifier.complete()