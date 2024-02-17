from progress_bar.base_progress_bar import BaseProgressBar
from futwiz.constants import NO_PLAYERS_PER_PAGE


class PlayersCompleteProgressBar(BaseProgressBar):

    def __init__(self, start_page_no, end_page_no, no_players_in_last_page):
        super().__init__()
        total_players = self._calculate_no_players_to_save(
            start_page_no,
            end_page_no,
            no_players_in_last_page
        )
        self._progressbar.total = total_players

    def _calculate_no_players_to_save(self, start_page_no, end_page_no, no_players_in_last_page):
        if start_page_no == end_page_no:
            no_iterations = no_players_in_last_page
        else:
            no_iterations = ((end_page_no - start_page_no) * NO_PLAYERS_PER_PAGE) + no_players_in_last_page
        return no_iterations
