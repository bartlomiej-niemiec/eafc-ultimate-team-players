import time
from threading import Lock
from futwiz.players_page.players_page_parser import PlayerPageParserFactory
from http import HTTPStatus
from utils.get_requests.get_request_factory import HttpGetRequestFactory
import config
from utils.proxy_servers import ProxyPool, get_proxy_servers_from_file
from fut_players.fut_players_mode import FutPlayersMode
from futwiz.players_page.util import PlayersPageType


class PageVisitor:

    @classmethod
    def work(cls, toolset):
        players_page_url = toolset.get_next_page_url()
        http_request = HttpGetRequestFactory.create(toolset.proxies if toolset.use_proxy() else None,
                                                    config.MAX_RETRIES)
        players_page_context = http_request.get(players_page_url)
        players_page_type = PlayersPageType.AllPlayers
        if config.FUT_PLAYERS_MODE == FutPlayersMode.LatestPlayerUpdate:
            players_page_type = PlayersPageType.LatestAddedPlayers
        players_page_parser = PlayerPageParserFactory.create(players_page_context, players_page_type)
        players = players_page_parser.get_players_ref_list()
        del players_page_parser
        for player_ref in players:
            player_page_context = http_request.get(player_ref.href)
            if http_request.get_status_code() == HTTPStatus.NOT_FOUND:
                continue
            player_ref.page_source = player_page_context
            toolset.add_to_csv_queue(player_ref)
            time.sleep(toolset.get_request_delay())
        del players


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
