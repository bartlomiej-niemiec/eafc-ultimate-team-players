from abc import ABC, abstractmethod


class PageCompleteObserver(ABC):

    @abstractmethod
    def update(self):
        pass