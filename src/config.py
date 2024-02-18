from fut_players.fut_players_mode import FutPlayersMode


class Config:
    # MODE
    """
     * In LatestPlayerUpdate mode there is 1 working thread and the common config only matter
     * In GetAllPlayers mode there is n working thread and the whole config matter
    """
    FUT_PLAYERS_MODE = FutPlayersMode.LatestPlayerUpdate

    # COMMON CONFIG
    # REQUESTS
    MAX_RETRIES = 20
    DELAY_TO_REQUESTS_RETRY_S = 3
    DELAY_TO_NEXT_REQUEST_S = 0

    # CSV LOGGING
    INCLUDE_PLAYER_STATS = True
    LOGGING_THREAD_DELAY_S = 0.05
    CSV_FILE_NAME = "fut_players.csv"

    # GET ALL PLAYERS CONFIG
    # PROXY SERVERS
    USE_PROXY = True
    PROXY_SERVERS_FILE_PATH = r""

    # THREADS
    NO_WORKING_THREADS = 10

    # PAGES
    START_PAGE = 0
    END_PAGE = None  # None means get all pages
