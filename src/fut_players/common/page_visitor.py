import time
from threading import Lock, Event
from futwiz.players_page.players_page_parser import PlayerPageParserFactory
from http import HTTPStatus


class PageVisitorWithStopEvent:

    @classmethod
    def work(cls, toolset, stop: Event):
        players_page_url = toolset.get_next_page_url()
        players_page_context = toolset.http_get_request.get(players_page_url)
        players_list = _get_players_list_from_page(players_page_context, toolset.get_players_page_type())
        for player_ref in players_list:
            if stop.is_set():
                break
            _visit_page_and_set_page_source(player_ref, toolset.http_request)
            if toolset.http_request.get_status_code() == HTTPStatus.NOT_FOUND:
                continue
            toolset.add_to_csv_queue(player_ref)
            time.sleep(toolset.get_request_delay())


class PageVisitor:

    @classmethod
    def work(cls, toolset):
        players_page_url = toolset.get_next_page_url()
        players_page_context = toolset.http_request.get(players_page_url)
        players_list = _get_players_list_from_page(players_page_context, toolset.get_players_page_type())
        for player_ref in players_list:
            _visit_page_and_set_page_source(player_ref, toolset.http_request)
            if toolset.http_request.get_status_code() == HTTPStatus.NOT_FOUND:
                continue
            toolset.add_to_csv_queue(player_ref)
            time.sleep(toolset.get_request_delay())


def _get_players_list_from_page(page_context, players_page_type):
    players_page_parser = PlayerPageParserFactory.create(page_context, players_page_type)
    return players_page_parser.get_players_ref_list()


def _visit_page_and_set_page_source(player_ref, http_get_request):
    player_page_context = http_get_request.get(player_ref.href)
    player_ref.page_source = player_page_context


class Toolset:

    def __init__(self, logging_queue, player_page_generator, delay, http_request, players_page_type):
        self._logging_queue = logging_queue
        self._player_page_generator = player_page_generator
        self.http_request = http_request
        self._delay = delay
        self._lock = Lock()
        self._players_page_type = players_page_type

    def add_to_csv_queue(self, player_data):
        return self._logging_queue.put(player_data)

    def get_request_delay(self):
        return self._delay

    def get_next_page_url(self):
        self._lock.acquire()
        page_url = self._player_page_generator.get_page_url()
        self._player_page_generator.next_page()
        self._lock.release()
        return page_url

    def get_players_page_type(self):
        return self._players_page_type
