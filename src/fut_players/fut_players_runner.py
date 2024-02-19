from fut_players.fut_players_mode import FutPlayersMode
from fut_players.standard.fut_players import FutPlayers
from src.fut_players.updater.fut_players_updater import FutPlayersUpdater
import config


class FutPlayersRunner:

    @classmethod
    def create(cls, mode):
        if mode == FutPlayersMode.LatestPlayerUpdate:
            return FutPlayersUpdater(config.LatestPlayerModeConfig)
        elif mode == FutPlayersMode.GetAllPlayers:
            return FutPlayers(config.GetAllPlayersModeConfig)