from sqlalchemy import create_engine


class DbEngineInstance:
    _instance = None

    @staticmethod
    def get_instance():
        if DbEngineInstance._instance is None:
            DbEngineInstance._instance = create_engine("sqlite+pysqlite:///fc_24_players.db", echo=True)
        instance = DbEngineInstance._instance
        return instance
