import tqdm
from fut_players.progress_bar.page_complete_observer import PlayerCompleteObserver
from futwiz.utils.constants import NO_PLAYERS_PER_PAGE

BAR_FORMAT = "{l_bar}{bar} [players: {n_fmt}/{total_fmt} time spent: {elapsed}]"
BAR_GREEN_COLOUR = 'green'


class FutCompleteProgressBar(PlayerCompleteObserver):

    def __init__(self, start_page_no, end_page_no, no_players_in_last_page):
        self._increment_value = 1
        total_players = self._calculate_no_players_to_get(
            start_page_no,
            end_page_no,
            no_players_in_last_page
        )
        self._progressbar = tqdm.tqdm(total=total_players, bar_format=BAR_FORMAT, colour=BAR_GREEN_COLOUR)

    def update(self):
        self._progressbar.update(self._increment_value)

    def _calculate_no_players_to_get(self, start_page_no, end_page_no, no_players_in_last_page):
        if start_page_no == end_page_no:
            no_iterations = no_players_in_last_page
        else:
            no_iterations = ((end_page_no - start_page_no) * NO_PLAYERS_PER_PAGE) + no_players_in_last_page
        return no_iterations
