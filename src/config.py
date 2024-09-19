from utils.ea_fc_versions import EaFcVersions


class CommonConfig:
    # REQUESTS
    MAX_RETRIES = 20
    DELAY_TO_REQUESTS_RETRY_S = 3
    DELAY_TO_NEXT_REQUEST_S = 0

    # CSV LOGGING
    INCLUDE_PLAYER_STATS = True
    LOGGING_THREAD_DELAY_S = 0.05
    CSV_FILEPATH = "../eafc25_ut_players.csv"

    # EAFCVERSION
    EA_FC_VERSION = EaFcVersions.EA_FC_25


class ProxyServersConfig:
    # PROXY SERVERS
    USE_PROXY = False
    PROXY_SERVERS_FILEPATH = r""

    # THREADS1
    NO_WORKING_THREADS = 10


class LatestPlayerModeConfig(CommonConfig):
    pass


class PriceUpdateConfig(CommonConfig, ProxyServersConfig):
    pass


class GetAllPlayersModeConfig(CommonConfig, ProxyServersConfig):
    # PAGES
    START_PAGE = 0
    END_PAGE = None  # None means get all pages


class CreateDbModeConfig(CommonConfig):
    pass
