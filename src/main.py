from fut_players.fut_players_runner import FutPlayers
from utils.config_parser import ConfigParser
import pathlib

if __name__ == "__main__":
    config_filepath = pathlib.Path().resolve()
    config_filepath = pathlib.Path().joinpath(config_filepath, "config.ini")
    config = ConfigParser(config_filepath)
    config.read()
    FutPlayers(config.get(), start_page_number=715).run()
