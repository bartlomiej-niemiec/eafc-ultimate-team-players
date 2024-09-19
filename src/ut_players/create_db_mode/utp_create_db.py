from ut_players.common.utp_base import UtpBase
from src.db.CsvToDbImporter import CsvToDbImporter
from src.db.DbEngineFactory import RDBMS
from src.utils.csv_utils import get_csv_content


class UtpCreateDbFromCsv(UtpBase):

    def __init__(self, config):
        super().__init__(config)

    def run(self):
        csv_content = get_csv_content(self._config.CSV_FILEPATH)
        self._init_progress_bar(csv_content.shape[0])
        self._init_player_progress_notification()
        csvtodbimporter = CsvToDbImporter(csv_content, RDBMS.SQLLITE3, self._player_save_notifier)
        csvtodbimporter.run()