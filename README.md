# FC24 FUT PLAYERS

This repository contains script to automatically fetch FC24 Ultimate Team players cards from [Futwiz](https://www.futwiz.com/en/fc24/) website.
Player card data include in game stats, market price, playstyles etc. 


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Usage
Script can be run in two modes:
* fetch all of the Ultimate Team cards and write them to csv file,
* write to csv file latest added players and stop at first card that is already in file.

To select which mode you would like to run set it in main.py:

```python
from fut_players.fut_players_runner import FutPlayersRunner
from fut_players.fut_players_mode import FutPlayersMode

if __name__ == "__main__":
    fut_players = FutPlayersRunner.create(FutPlayersMode.LatestPlayerUpdate)
    fut_players.run()

```
Each run of script can be configured in **config.py** im term of:
* using proxy servers (only in first mode - getting all of the players),
* number of working/scraping threads (only in first mode - getting all of the players),
* csv filepath,
* max retries of http get request,
* time delay to next request\time delay between each retry.