from sqlalchemy import create_engine
from src.db.DbFactory import Fc24PlayersDbFactory
from src.utils.csv_utils import get_csv_content, CsvIterator
from src.utils.ea_fc_card import FcPlayerCardFactory
from src.config import CommonConfig

if __name__ == "__main__":
    engine = create_engine("sqlite+pysqlite:///fc_24_players.db", echo=True)
    Fc24PlayersDbFactory.create_db(engine)
    csv_content = get_csv_content("../" + CommonConfig.CSV_FILEPATH)
    csv_iterator = CsvIterator(csv_content)
    for row in csv_iterator:
        card = FcPlayerCardFactory.create(row)
        print(card.__dict__)


