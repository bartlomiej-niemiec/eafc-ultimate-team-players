import tqdm
from fut_players.progress_bar.page_complete_observer import PageCompleteObserver
from futwiz.utils.constants import NO_PLAYERS_PER_PAGE


class FutCompleteProgressBar(PageCompleteObserver):

    def __init__(self, start_page_no, end_page_no, no_players_in_last_page):
        self._start_page_no = start_page_no
        self._end_page_no = end_page_no
        self._increment = 1
        if self._start_page_no == self._end_page_no:
            no_iterations = no_players_in_last_page
        else:
            no_iterations = (self._end_page_no - self._start_page_no - 1) * NO_PLAYERS_PER_PAGE + no_players_in_last_page
        self._progressbar = tqdm.tqdm(total=no_iterations)

    def update(self):
        self._progressbar.update(self._increment)
