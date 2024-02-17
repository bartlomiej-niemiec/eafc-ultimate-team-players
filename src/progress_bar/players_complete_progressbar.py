import tqdm
from progress_bar.player_save_observer import PlayerSaveObserver
from futwiz.constants import NO_PLAYERS_PER_PAGE

BAR_FORMAT = "{l_bar}{bar} [players: {n_fmt}/{total_fmt} time spent: {elapsed}]"
BAR_GREEN_COLOUR = 'green'


class PlayersCompleteProgressBar(PlayerSaveObserver):

    def __init__(self, total_iterations, bar_format=BAR_FORMAT):
        self._increment_value = 1
        self._progressbar = tqdm.tqdm(bar_format=bar_format, colour=BAR_GREEN_COLOUR, total=total_iterations)

    def update(self):
        self._progressbar.update(self._increment_value)

    @staticmethod
    def calculate_no_players_to_save(start_page_no, end_page_no, no_players_in_last_page):
        if start_page_no == end_page_no:
            no_iterations = no_players_in_last_page
        else:
            no_iterations = ((end_page_no - start_page_no) * NO_PLAYERS_PER_PAGE) + no_players_in_last_page
        return no_iterations
