from http import HTTPStatus

from futwiz.players_page.player_ref import PlayerRef


class PlayerVisitorToolset:

    def __init__(self, logging_queue, http_request, player_getter):
        self._logging_queue = logging_queue
        self.http_request = http_request
        self._player_getter = player_getter

    def add_to_csv_queue(self, player_data):
        return self._logging_queue.put(player_data)

    def get_next_player_url(self):
        return self._player_getter.get_next_url()


class PlayerVisitor:

    @classmethod
    def visit(cls, toolset: PlayerVisitorToolset):
        while player_page_url := toolset.get_next_player_url():
            player_ref = PlayerRef(player_page_url)
            page_source = toolset.http_request.get(player_page_url)
            if toolset.http_request.get_status_code() == HTTPStatus.NOT_FOUND:
                return
            player_ref.page_source = page_source
            toolset.add_to_csv_queue(player_ref)
