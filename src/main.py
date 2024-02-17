from fut_players.fut_players_runner import FutPlayersRunner
from config import FUT_PLAYERS_MODE

if __name__ == "__main__":
    fut_players = FutPlayersRunner.create(FUT_PLAYERS_MODE)
    fut_players.run()
