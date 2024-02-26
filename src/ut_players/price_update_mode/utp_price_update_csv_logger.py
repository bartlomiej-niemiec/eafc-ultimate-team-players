import time
from threading import Event
from ut_players.common.file_logger_base import FileLogger
from ut_players.common.utils import does_file_include_player_stats, get_csv_content
from futwiz.player_page.player_page_parser import PlayerDataParser
from futwiz.player_page.player_data_template import GeneralPlayerData


class PriceUpdateLogger(FileLogger):

    def __init__(self, player_ref_queue, filepath, player_complete_notifier, thread_interval_s):
        super(PriceUpdateLogger, self).__init__()
        self._thread_interval_s = thread_interval_s
        self._player_ref_queue = player_ref_queue
        self._stop_event = Event()
        self._player_data_parser = PlayerDataParser()
        self._filepath = filepath
        self._csv_content = None
        self._player_complete_notifier = player_complete_notifier
        self._with_player_stats = does_file_include_player_stats(filepath)
        self._map_futwiz_link = dict()

    def run(self):
        self._read_csv_content()
        self._logger()

    def stop(self):
        self._stop_event.set()

    def _read_csv_content(self):
        self.csv_content = get_csv_content(self._filepath)
        self._map_futwiz_link_to_csv_row_index()

    def _save_back_to_csv(self):
        self.csv_content.to_csv(self._filepath, sep=';', encoding='utf-8', mode='w', header=None, index=False)

    def _logger(self):
        while not self._stop_event.is_set():
            if not self._player_ref_queue.empty():
                player_ref = self._player_ref_queue.get()
                player_data = self._get_player_data(player_ref)
                self.csv_content.loc[self._map_futwiz_link[player_ref.href], GeneralPlayerData.Price] = player_data[GeneralPlayerData.Price]
                self._player_complete_notifier.complete()
                time.sleep(self._thread_interval_s)
        self._save_back_to_csv()

    def _get_player_data(self, player_ref):
        return self._player_data_parser.parse_and_get_player_data(
            player_ref.page_source,
            False
        )

    def _map_futwiz_link_to_csv_row_index(self):
        for row, series in self.csv_content.iterrows():
            if row > 0:
                self._map_futwiz_link[series[GeneralPlayerData.FutwizLink]] = row