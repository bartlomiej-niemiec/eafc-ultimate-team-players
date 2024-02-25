from fut_players.fut_players_mode import FutPlayersMode
from fut_players.standard.fut_players import FutPlayers
from fut_players.player_db_update.fut_players_db_updater import FutPlayersUpdater
from fut_players.price_update.fut_players_price_update import FutPlayersPriceUpdater
import config


class FutPlayersRunner:

    @classmethod
    def create(cls, mode):
        if mode == FutPlayersMode.LatestPlayerUpdate:
            return FutPlayersUpdater(config.LatestPlayerModeConfig)
        elif mode == FutPlayersMode.GetAllPlayers:
            return FutPlayers(config.GetAllPlayersModeConfig)
        elif mode == FutPlayersMode.PriceUpdate:
            return FutPlayersPriceUpdater(config.PriceUpdateConfig)