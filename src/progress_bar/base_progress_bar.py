import tqdm
from progress_bar.player_save_observer import PlayerSaveObserver

BAR_FORMAT = "{l_bar}{bar} [players: {n_fmt}/{total_fmt} time spent: {elapsed}]"
BAR_GREEN_COLOUR = 'green'


class BaseProgressBar(PlayerSaveObserver):

    def __init__(self):
        self._increment_value = 1
        self._progressbar = tqdm.tqdm(bar_format=BAR_FORMAT, colour=BAR_GREEN_COLOUR)

    def update(self):
        self._progressbar.update(self._increment_value)
