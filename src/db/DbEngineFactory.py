from sqlalchemy import create_engine


class RDBMS:
    SQLLITE3 = 0


class RDBMSNotSupported(Exception):
    pass


class DbEngineFactory:

    @staticmethod
    def create(db):
        if RDBMS.SQLLITE3 == db:
            return create_engine("sqlite+pysqlite:///fc_24_players.db", echo=True)
        else:
            raise RDBMSNotSupported("Selected DB is not supported")
