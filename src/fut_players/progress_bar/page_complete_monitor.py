from threading import Lock


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
            observer.update()