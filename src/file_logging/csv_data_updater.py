import time
import config
import pandas as pd
import csv

from threading import Thread, Event
from futwiz.player_page.player_data_template import GeneralPlayerData, PlayerDataTemplateFactory, CommonPosStats
from futwiz.player_page.player_page_parser import PlayerDataParser

LOGGER_THREAD_DELAY = config.LOGGING_THREAD_DELAY_S
FILES_NAME = config.CSV_FILE_NAME


class CsvUpdater(Thread):

    def __init__(self, player_ref_queue, filepath, no_more_to_update: Event, player_complete_notifier):
        super(CsvUpdater, self).__init__()
        self.player_ref_queue = player_ref_queue
        self._no_more_to_update = no_more_to_update
        self._stop_event = Event()
        self._player_data_parser = PlayerDataParser()
        self._filepath = filepath
        self._csv_content = None
        self._player_complete_notifier = player_complete_notifier
        self._with_player_stats = self._is_file_include_player_stats()
        self._headers = PlayerDataTemplateFactory().create(self._with_player_stats).keys()

    def run(self):
        self._read_csv_content()
        self._logger()

    def stop(self):
        self._stop_event.set()

    def _logger(self):
        while not self._no_more_to_update.is_set():
            if self._stop_event.isSet():
                break
            if not self.player_ref_queue.empty():
                player_ref = self.player_ref_queue.get()
                player_in_csv = self.csv_content[GeneralPlayerData.FutwizLink].eq(player_ref.href.strip()).any()
                if not player_in_csv:
                    self._parser_player_data_and_save(player_ref)
                else:
                    self._no_more_to_update.set()
                    break
                time.sleep(LOGGER_THREAD_DELAY)

    def _read_csv_content(self):
        names = [key for key in PlayerDataTemplateFactory().create(self._with_player_stats).keys()]
        self.csv_content = pd.read_csv(self._filepath, delimiter=';', names=names)

    def _parser_player_data_and_save(self, player_ref):
        player_data = self._player_data_parser.parse_and_get_player_data(
            player_ref.page_source,
            self._with_player_stats
        )
        player_data.update(player_ref.get_dict())
        with open(self._filepath, 'a', newline='', encoding="utf-8") as csvfile:
            csv_dictwriter = csv.DictWriter(csvfile, fieldnames=self._headers)
            csv_dictwriter.writerow(player_data)
        self._player_complete_notifier.complete()

    def _is_file_include_player_stats(self):
        HEADERS_ROW = 0
        with open(self._filepath, 'r', newline='', encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = next(csv_reader)
        first_key = list(CommonPosStats.get_dict_template().keys())[0]
        return True if first_key in headers else False