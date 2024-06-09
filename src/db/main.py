from src.db.CsvToDbImporter import CsvToDbImporter
from src.db.DbEngineFactory import RDBMS
from src.utils.csv_utils import get_csv_content

import pathlib


if __name__ == "__main__":

    CSV_FILENAME = "fut_players.csv"
    CSV_FILEPATH = pathlib.Path(__file__).parent.parent.parent.resolve().joinpath(CSV_FILENAME)
    csv_content = get_csv_content(CSV_FILEPATH)

    csvtodbimporter = CsvToDbImporter(csv_content, RDBMS.SQLLITE3)
    csvtodbimporter.run()