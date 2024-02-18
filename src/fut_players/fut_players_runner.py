from fut_players.fut_players_mode import FutPlayersMode
from fut_players.standard.fut_players import FutPlayers
from src.fut_players.updater.fut_players_updater import FutPlayersUpdater


class FutPlayersRunner:

    @classmethod
    def create(cls, config):
        if config.FUT_PLAYERS_MODE == FutPlayersMode.LatestPlayerUpdate:
            return FutPlayersUpdater(config)
        elif config.FUT_PLAYERS_MODE == FutPlayersMode.GetAllPlayers:
            return FutPlayers(config)