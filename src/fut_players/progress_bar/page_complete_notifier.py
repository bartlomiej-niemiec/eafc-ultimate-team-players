from threading import Lock


class PlayerCompleteNotifier:

    def __init__(self):
        self._lock = Lock()
        self._observers = []

    def increment(self):
        self._lock.acquire()
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