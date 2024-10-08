from ut_players.ut_players_mode import UtPlayersMode
from ut_players.all_players_mode.utp_get_all_players import UtpGetAllPlayers
from ut_players.latest_player_mode.utp_latest_players_update import UtpLatestPlayersUpdate
from ut_players.price_update_mode.utp_price_update import FutPlayersPriceUpdater
from ut_players.create_db_mode.utp_create_db import UtpCreateDbFromCsv
import config


class UtPlayersRunnerFactory:

    @classmethod
    def create(cls, mode):
        if mode == UtPlayersMode.LatestPlayerUpdate:
            return UtpLatestPlayersUpdate(config.CreateDbModeConfig)
        elif mode == UtPlayersMode.GetAllPlayers:
            return UtpGetAllPlayers(config.GetAllPlayersModeConfig)
        elif mode == UtPlayersMode.PriceUpdate:
            return FutPlayersPriceUpdater(config.PriceUpdateConfig)
        elif mode == UtPlayersMode.CreateDbFromCsv:
            return UtpCreateDbFromCsv(config.CreateDbModeConfig)