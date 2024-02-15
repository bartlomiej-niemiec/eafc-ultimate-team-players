import time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from futwiz.players_page import PlayersPageParser, PlayersPageUrlGenerator
from utils.get_request import GetRequest, ErrorCode
import asyncio
import config
from utils.proxy_servers import ProxyPool, get_proxy_servers_from_file


class Worker:

    @classmethod
    def work(cls, toolset):
        page_url = toolset.get_next_page_url()
        get_request = GetRequest(toolset.proxies, config.MAX_RETRIES, config.DELAY_BETWEEN_TO_RETRY)
        page_context = get_request.send(page_url, toolset.use_proxy())
        players_page = PlayersPageParser(page_context)
        players = players_page.get_players_ref_list()
        del players_page
        for player in players:
            page_context = get_request.send(player.href, toolset.use_proxy())
            if get_request.error_code == ErrorCode.HTTP_NOT_FOUND:
                continue
            player.page_source = page_context
            toolset.add_to_csv_queue(player)
            time.sleep(toolset.get_request_delay())
        del players


class Supervisor:

    def __init__(self, csv_logging_queue, start_page_no, last_page_no):
        self._worker_toolset = WorkerToolset(
            csv_logging_queue,
            PlayersPageUrlGenerator(start_page_no),
        )
        self._no_pages_to_work = last_page_no - start_page_no + 1
        self._no_workers = config.NO_WORKING_THREADS

    def start(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._get_work_done())
        loop.run_until_complete(future)

    async def _get_work_done(self):
        with ThreadPoolExecutor(max_workers=self._no_workers) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    Worker.work,
                    self._worker_toolset
                )
                for _ in range(self._no_pages_to_work)
            ]

        return await asyncio.gather(*tasks)


class WorkerToolset:

    def __init__(self, logging_queue, player_page_generator):
        self._logging_queue = logging_queue
        self._player_page_generator = player_page_generator
        self.proxies = None
        if config.USE_PROXY:
            self.proxies = self._proxies = ProxyPool(
                get_proxy_servers_from_file(
                    config.PROXY_SERVERS_FILE_PATH
                )
            )
        self._lock = Lock()

    def add_to_csv_queue(self, player_data):
        return self._logging_queue.put(player_data)

    def get_request_delay(self):
        return config.DELAY_BETWEEN_REQUESTS_S

    def get_next_page_url(self):
        self._lock.acquire()
        page_url = self._player_page_generator.get_page_url()
        self._player_page_generator.next_page()
        self._lock.release()
        return page_url

    def use_proxy(self):
        return config.USE_PROXY
