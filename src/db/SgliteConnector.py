import sqlite3
from sqlite3 import Error

from src.db.DbConnectionIf import DbConnectorIf, ConnectionCreateFailed


class SqliteConnector(DbConnectorIf):

    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self._path)
        except Error as e:
            ConnectionCreateFailed(f"The error '{e}' occurred")

        return connection
