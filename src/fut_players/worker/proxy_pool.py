from threading import Lock


class ProxyPool:

    def __init__(self, proxies):
        self._lock = Lock()
        self._proxies = proxies

    def alloc(self):
        self._lock.acquire()
        proxy = self._proxies.pop(0)
        self._lock.release()
        return proxy

    def dealloc(self, proxy):
        self._lock.acquire()
        self._proxies.push_back(proxy)
        self._lock.release()