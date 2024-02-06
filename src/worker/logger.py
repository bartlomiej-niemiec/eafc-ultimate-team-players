from multiprocessing import Lock


class Logger:

    def __init__(self):
        self._lock = Lock()

    def log(self, msg):
        self._lock.acquire()
        print(msg)
        self._lock.release()
