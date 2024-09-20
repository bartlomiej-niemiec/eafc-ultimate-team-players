# EAFC Ultimate Team PLAYERS

This repository contains script to automatically fetch EAFC Ultimate Team players cards from [Futwiz](https://www.futwiz.com) website.
Player card data include in game stats, market price, playstyles etc. 

# Supported EAFC versions

* EAFC24,
* EAFC25

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Usage
Script can be run in three modes:
* fetch all of the Ultimate Team cards and write them to csv file,
* write to csv file latest added players and stop at first card that is already in file.
* update the price for all of the players in csv file.

To select which mode you would like to run set it in main.py:

```python
from ut_players.ut_players_factory import UtPlayersRunnerFactory
from ut_players.ut_players_mode import UtPlayersMode

if __name__ == "__main__":
    fut_players = UtPlayersRunnerFactory.create(UtPlayersMode.LatestPlayerUpdate)
    fut_players.run()

```
Each run of script can be configured in **config.py** im term of:
* eafc version,
* using proxy servers (getting all of the players and price update mode),
* number of working/scraping threads (getting all of the players and price update mode),
* csv filepath,
* max retries of http get request,
* time delay to next request\time delay between each retry.

How proxy servers .txt file should look like:
```bash
<address_ip>:<port>
<address_ip>:<port>
<address_ip>:<port>
<address_ip>:<port>
```

