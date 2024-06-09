from src.db.Models import *


class Fc24PlayersTablesFactory:

    @staticmethod
    def create(engine):
        Base.metadata.create_all(bind=engine)
