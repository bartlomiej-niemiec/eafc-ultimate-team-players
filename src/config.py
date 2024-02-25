class CommonConfig:
    # REQUESTS
    MAX_RETRIES = 20
    DELAY_TO_REQUESTS_RETRY_S = 3
    DELAY_TO_NEXT_REQUEST_S = 0

    # CSV LOGGING
    INCLUDE_PLAYER_STATS = True
    LOGGING_THREAD_DELAY_S = 0.05
    CSV_FILE_NAME = "../fut_players.csv"


class ProxyServersConfig:
    # PROXY SERVERS
    USE_PROXY = True
    PROXY_SERVERS_FILE_PATH = r""

    # THREADS1
    NO_WORKING_THREADS = 10


class LatestPlayerModeConfig(CommonConfig):
    pass


class PriceUpdateConfig(CommonConfig, ProxyServersConfig):
    pass


class GetAllPlayersModeConfig(CommonConfig, ProxyServersConfig):
    # PAGES
    START_PAGE = 0
    END_PAGE = 2  # None means get all pages
