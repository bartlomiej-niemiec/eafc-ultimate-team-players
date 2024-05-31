from abc import ABC, abstractmethod


class ConnectionCreateFailed(Exception):
    pass


class DbConnectorIf(ABC):

    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path

    @abstractmethod
    def create_connection(self):
        pass
