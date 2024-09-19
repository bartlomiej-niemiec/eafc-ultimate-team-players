from sqlalchemy.orm import Session

from db.DbEaFcCardInsertion import DbEaFcCardInsertion
from db.DbEngineFactory import DbEngineFactory
from db.Fc24PlayersTablesFactory import Fc24PlayersTablesFactory
from utils.csv_utils import CsvIterator
from utils.ea_fc_card import FcPlayerCardFactory


class CsvToDbImporter:

    def __init__(self, csv_content, rdbms, player_save_notifier):
        self._csv_content = csv_content
        self._rdbms_engine = DbEngineFactory.create(rdbms)
        self._player_save_notifier = player_save_notifier

    def set_csv_content(self, csv_content):
        self._csv_content = csv_content

    def run(self):
        Fc24PlayersTablesFactory.create(self._rdbms_engine)
        fut_players_csv_iterator = CsvIterator(self._csv_content)
        with Session(self._rdbms_engine) as session:
            dbcardinsertion = DbEaFcCardInsertion(session)
            with session.begin():
                for player_info_list in fut_players_csv_iterator:
                    card = FcPlayerCardFactory.create(player_info_list)
                    dbcardinsertion.insert_card(card)
                    self._player_save_notifier.complete()
