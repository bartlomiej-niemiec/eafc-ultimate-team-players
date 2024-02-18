from fut_players.fut_players_runner import FutPlayersRunner
from config import Config

if __name__ == "__main__":
    fut_players = FutPlayersRunner.create(Config)
    fut_players.run()
