import configparser


class ConfigKeys:
    USE_PROXY = "use_proxy"
    PROXY_SERVERS_FILE_PATH = "proxy_servers_file_path"
    NO_WORKING_THREADS = "no_working_threads"
    DELAY_BETWEEN_REQUESTS_S = "delay_between_requests"


class ConfigParser:

    def __init__(self, filepath):
        self._config_parser = configparser.ConfigParser()
        self._config_parser.read(filepath)
        self._config = dict()

    def read(self):
        self._config[ConfigKeys.USE_PROXY] = self._config_parser["PROXY_SERVERS"]["USE_PROXY"].lower() == 'true'
        self._config[ConfigKeys.PROXY_SERVERS_FILE_PATH] = self._config_parser["PROXY_SERVERS"][
            "PROXY_SERVERS_FILE_PATH"]

        self._config[ConfigKeys.NO_WORKING_THREADS] = int(self._config_parser["THREADS"]["NO_WORKING_THREADS"])
        self._config[ConfigKeys.DELAY_BETWEEN_REQUESTS_S] = int(self._config_parser["THREADS"]["DELAY_BETWEEN_REQUESTS_S"])

    def get(self):
        return Config(self._config)


class Config:

    def __init__(self, config):
        self._config = config

    def use_proxy(self):
        return self._config[ConfigKeys.USE_PROXY]

    def get_proxy_servers_filepath(self):
        return self._config[ConfigKeys.PROXY_SERVERS_FILE_PATH]

    def get_no_working_threads(self):
        return self._config[ConfigKeys.NO_WORKING_THREADS]

    def get_request_delay(self):
        return self._config[ConfigKeys.DELAY_BETWEEN_REQUESTS_S]

