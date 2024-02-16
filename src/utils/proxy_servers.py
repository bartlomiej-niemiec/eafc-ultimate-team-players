from threading import Lock


def get_proxy_servers_from_file(file_path):
    proxies = list()
    with open(file_path, "r") as f:
        proxies = [{"http": line.strip()} for line in f]
    return proxies


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
        self._proxies.append(proxy)
        self._lock.release()
