from fut_players.fut_players_runner import FutPlayersRunner
from fut_players.fut_players_mode import FutPlayersMode

if __name__ == "__main__":
    fut_players = FutPlayersRunner.create(FutPlayersMode.PriceUpdate)
    fut_players.run()
