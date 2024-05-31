from src.db.DbConnectionIf import DbConnectorIf
from src.db.DbSchema import SCHEMA_SQL


class Fc24PlayersDbFactory:

    _CREATE_STATEMENT_PREFIX = "CREATE TABLE"
    _CREATE_STATEMENT_SUFFIX = ");"

    def __init__(self, db_connector: DbConnectorIf):
        self._db_connection = db_connector

    def create_db(self):
        self._db_connection.path = "fc_24_players.db"
        connection = self._db_connection.create_connection()
        self._create_tables(connection)

    def _create_tables(self, connection):
        statement = ""
        statement_found = False
        for char in SCHEMA_SQL:
            statement += char
            if not statement_found and Fc24PlayersDbFactory._CREATE_STATEMENT_PREFIX in statement:
                statement_found = True
            elif statement_found and Fc24PlayersDbFactory._CREATE_STATEMENT_SUFFIX in statement:
                connection.execute(statement)
                statement = ""
