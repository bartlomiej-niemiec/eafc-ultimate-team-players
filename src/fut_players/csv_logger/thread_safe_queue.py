from queue import Queue
from multiprocessing import Lock


class ThreadSafeQueue:

    def __init__(self):
        self._queue = Queue()
        self._lock = Lock()

    def get(self):
        self._lock.acquire()
        object = self._queue.get()
        self._lock.release()
        return object

    def put(self, object):
        self._lock.acquire()
        self._queue.put(object)
        self._lock.release()

    def empty(self):
        return self._queue.empty()