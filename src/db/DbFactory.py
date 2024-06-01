from src.db.Models import *


class Fc24PlayersDbFactory:

    @staticmethod
    def create_db(engine):
        Base.metadata.create_all(bind=engine)