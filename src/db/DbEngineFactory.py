from sqlalchemy import create_engine


class RDBMS:
    SQLLITE3 = 0


class RDBMSNotSupported(Exception):
    pass


class DbEngineFactory:

    @staticmethod
    def create(db, ea_fc_version):
        db_name = f"eafc_{str(ea_fc_version)}_players.db"
        if RDBMS.SQLLITE3 == db:
            return create_engine(f"sqlite+pysqlite:///../{db_name}", echo=False)
        else:
            raise RDBMSNotSupported("Selected DB is not supported")
