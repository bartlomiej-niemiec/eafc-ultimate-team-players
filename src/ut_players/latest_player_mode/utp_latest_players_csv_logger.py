import time
import csv

from threading import Event
from ut_players.common.file_logger_base import FileLogger
from ut_players.common.utils import does_file_include_player_stats
from utils.csv_utils import get_csv_content
from futwiz.player_page.player_data_template import GeneralPlayerData, PlayerDataTemplateFactory
from futwiz.player_page.player_page_parser import PlayerDataParser


class LatestPlayersLogger(FileLogger):

    def __init__(self, player_ref_queue, filepath, no_more_to_update: Event, player_complete_notifier,
                 thread_interval_s, ea_fc_version):
        super(LatestPlayersLogger, self).__init__()
        self._thread_interval_s = thread_interval_s
        self._player_ref_queue = player_ref_queue
        self._no_more_to_update = no_more_to_update
        self._stop_event = Event()
        self._player_data_parser = PlayerDataParser(ea_fc_version)
        self._filepath = filepath
        self._csv_content = None
        self._player_complete_notifier = player_complete_notifier
        self._with_player_stats = does_file_include_player_stats(filepath)
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
            if not self._player_ref_queue.empty():
                player_ref = self._player_ref_queue.get()
                player_in_csv = self.csv_content[GeneralPlayerData.FutwizLink].eq(player_ref.href.strip()).any()
                if not player_in_csv:
                    self._parser_player_data_and_save(player_ref)
                else:
                    self._no_more_to_update.set()
                    break
                time.sleep(self._thread_interval_s)

    def _read_csv_content(self):
        self.csv_content = get_csv_content(self._filepath)

    def _parser_player_data_and_save(self, player_ref):
        player_data = self._player_data_parser.parse_and_get_player_data(
            player_ref.page_source,
            self._with_player_stats
        )
        player_data.update(player_ref.get_dict())
        with open(self._filepath, 'a', newline='', encoding="utf-8") as csvfile:
            csv_dictwriter = csv.DictWriter(csvfile, fieldnames=self._headers, delimiter=';')
            csv_dictwriter.writerow(player_data)
        self._player_complete_notifier.complete()


