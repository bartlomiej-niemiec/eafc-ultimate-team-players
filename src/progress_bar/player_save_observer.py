from abc import ABC, abstractmethod


class PlayerSaveObserver(ABC):

    @abstractmethod
    def update(self):
        pass
