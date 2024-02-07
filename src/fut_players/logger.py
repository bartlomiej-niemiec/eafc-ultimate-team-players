import time
from abc import ABC, abstractmethod
from threading import Thread, Event, Lock
import progressbar


class Logger(Thread):

    def __init__(self, shared_queue):
        super(Logger, self).__init__()
        self.shared_queue = shared_queue
        self._stop_event = Event()

    def run(self):
        self._logger()

    def stop(self):
        self._stop_event.set()

    def _logger(self):
        queue_object = None
        while True:
            if self._stop_event.isSet():
                break
            if not self.shared_queue.empty():
                queue_object = self.shared_queue.get()
                print(queue_object)
            time.sleep(0.5)


class PageCompleteObserver(ABC):

    @abstractmethod
    def update(self, completed_pages):
        pass


class PageCompleteMonitor:

    def __init__(self):
        self._completed_pages = 0
        self._lock = Lock()
        self._observers = []

    def complete(self):
        self._lock.acquire()
        self._completed_pages += 1
        self._NotifyObservers()
        self._lock.release()

    def RegisterObserver(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def UnregisterObserver(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _NotifyObservers(self):
        for observer in self._observers:
            observer.update(self._completed_pages)


class FutCompleteProgressBar(PageCompleteObserver):

    def __init__(self, start_page_no, end_page_no):
        self._lock = Lock()
        self._start_page_no = start_page_no
        self._end_page_no = end_page_no
        widgets = [
            ' [', progressbar.Timer(), '] ',
            progressbar.Percentage(),
        ]
        self._progressbar = progressbar.ProgressBar(maxval=self._end_page_no, widgets=widgets)
        self._progressbar.start()
        self._progressbar.update(0)

    def update(self, completed_pages):
        update = completed_pages - self._start_page_no
        self._progressbar.update(update)
