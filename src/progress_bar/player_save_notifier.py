from threading import Lock


class PlayerSaveNotifier:

    def __init__(self):
        self._lock = Lock()
        self._observers = []

    def complete(self):
        self._lock.acquire()
        self._notify_observers()
        self._lock.release()

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self):
        for observer in self._observers:
            observer.update()