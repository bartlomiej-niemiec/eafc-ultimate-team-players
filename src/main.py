from ut_players.ut_players_factory import UtPlayersRunnerFactory
from ut_players.ut_players_mode import UtPlayersMode

if __name__ == "__main__":
    fut_players = UtPlayersRunnerFactory.create(UtPlayersMode.LatestPlayerUpdate)
    fut_players.run()
