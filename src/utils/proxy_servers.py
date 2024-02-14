from threading import Lock


def get_proxy_servers_from_file(file_path):
    proxies = list()
    with open(file_path, "r") as f:
        for line in f:
            stripped_line = line.strip()
            proxies.append(
                {
                    "http": stripped_line
                }
            )
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
