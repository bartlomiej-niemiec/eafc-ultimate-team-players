import time
from threading import Lock, Event
from futwiz.players_page.players_page_parser import PlayerPageParserFactory
from http import HTTPStatus
from utils.get_requests.get_request_factory import HttpGetRequestFactory
import config
from utils.proxy_servers import ProxyPool, get_proxy_servers_from_file
from fut_players.fut_players_mode import FutPlayersMode
from futwiz.players_page.util import PlayersPageType


class PageVisitorWithStopEvent:

    @classmethod
    def work(cls, toolset, stop: Event):
        players_page_url = toolset.get_next_page_url()
        http_request = HttpGetRequestFactory.create(toolset.proxies if toolset.use_proxy() else None,
                                                    config.MAX_RETRIES)
        players_list = _get_players_list_from_page(players_page_url, http_request)
        for player_ref in players_list:
            if stop.is_set():
                break
            _visit_page_and_set_page_source(player_ref, http_request)
            if http_request.get_status_code() == HTTPStatus.NOT_FOUND:
                continue
            toolset.add_to_csv_queue(player_ref)
            time.sleep(toolset.get_request_delay())


class PageVisitor:

    @classmethod
    def work(cls, toolset):
        players_page_url = toolset.get_next_page_url()
        http_request = HttpGetRequestFactory.create(toolset.proxies if toolset.use_proxy() else None,
                                                    config.MAX_RETRIES)
        players_list = _get_players_list_from_page(players_page_url, http_request)
        for player_ref in players_list:
            _visit_page_and_set_page_source(player_ref, http_request)
            if http_request.get_status_code() == HTTPStatus.NOT_FOUND:
                continue
            toolset.add_to_csv_queue(player_ref)
            time.sleep(toolset.get_request_delay())


def _get_players_list_from_page(page_url, http_get_request):
    players_page_context = http_get_request.get(page_url)
    players_page_type = PlayersPageType.AllPlayers
    if config.FUT_PLAYERS_MODE == FutPlayersMode.LatestPlayerUpdate:
        players_page_type = PlayersPageType.LatestAddedPlayers
    players_page_parser = PlayerPageParserFactory.create(players_page_context, players_page_type)
    return players_page_parser.get_players_ref_list()


def _visit_page_and_set_page_source(player_ref, http_get_request):
    player_page_context = http_get_request.get(player_ref.href)
    player_ref.page_source = player_page_context


class Toolset:

    def __init__(self, logging_queue, player_page_generator):
        self._logging_queue = logging_queue
        self._player_page_generator = player_page_generator
        self.proxies = None
        if config.USE_PROXY and config.FUT_PLAYERS_MODE != FutPlayersMode.LatestPlayerUpdate:
            self.proxies = self._proxies = ProxyPool(
                get_proxy_servers_from_file(
                    config.PROXY_SERVERS_FILE_PATH
                )
            )
        self._lock = Lock()

    def add_to_csv_queue(self, player_data):
        return self._logging_queue.put(player_data)

    def get_request_delay(self):
        return config.DELAY_TO_NEXT_REQUEST_S

    def get_next_page_url(self):
        self._lock.acquire()
        page_url = self._player_page_generator.get_page_url()
        self._player_page_generator.next_page()
        self._lock.release()
        return page_url

    def use_proxy(self):
        return config.USE_PROXY and config.FUT_PLAYERS_MODE != FutPlayersMode.LatestPlayerUpdate
