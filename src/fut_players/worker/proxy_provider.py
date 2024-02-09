import requests
from bs4 import BeautifulSoup
import json


DIV_PROXY_SERVER = "spy1x"
TR_TAG = "tr"

HTTP_PROXIES = [
    {"http": "http://bjzvjwwb:6gyibfuuixex@38.154.227.167:5868"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@185.199.229.156:7492"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@185.199.228.220:7300"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@185.199.231.45:8382"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@188.74.210.207:6286"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@188.74.183.10:8279"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@188.74.210.21:6100"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@45.155.68.129:8133"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@154.95.36.199:6893"},
    {"http": "http://bjzvjwwb:6gyibfuuixex@45.94.47.66:8110"}
]


class ProxyProvider:

    def __init__(self):
        self._proxies = HTTP_PROXIES#[{"http": f"{proxy['ip']}:{proxy['port']}"} for proxy in self.proxies_json]

    def get_proxy_servers(self):
        return self._proxies