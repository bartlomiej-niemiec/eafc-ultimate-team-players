from abc import ABC, abstractmethod


class PlayerCompleteObserver(ABC):

    @abstractmethod
    def update(self):
        pass
