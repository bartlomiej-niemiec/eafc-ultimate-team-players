from sqlalchemy.orm import Session

from src.db.DbEngineInstance import DbEngineInstance
from src.db.DbFactory import Fc24PlayersDbFactory, DbEaFcCardInsert

from src.utils.csv_utils import get_csv_content, CsvIterator
from src.utils.ea_fc_card import FcPlayerCardFactory

import pathlib


if __name__ == "__main__":
    CSV_FILENAME = "fut_players.csv"
    CSV_FILEPATH = pathlib.Path(__file__).parent.parent.parent.resolve().joinpath(CSV_FILENAME)

    engine = DbEngineInstance.get_instance()
    Fc24PlayersDbFactory.create_db(engine)

    csv_content = get_csv_content(CSV_FILEPATH)

    fut_players_csv_iterator = CsvIterator(csv_content)
    with Session(engine) as session:
        card_inserted = DbEaFcCardInsert(session)
        with session.begin():
            for player_info_list in fut_players_csv_iterator:
                card = FcPlayerCardFactory.create(player_info_list)
                card_inserted.insert_card(card)
