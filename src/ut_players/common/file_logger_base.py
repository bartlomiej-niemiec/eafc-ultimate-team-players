from abc import ABC, abstractmethod
from threading import Thread


class FileLogger(Thread, ABC):

    def __init__(self):
        super(FileLogger, self).__init__()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass
