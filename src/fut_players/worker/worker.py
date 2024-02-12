import time

from futwiz.players_page.futwiz_players_page_url import PlayersPageUrlGenerator
from utils.constants import NO_WORKERS
from concurrent.futures import ThreadPoolExecutor
from futwiz.players_page.futwiz_players_page import PlayersPage
from utils.get_requests import GetRequest, ErrorCode
from fut_players.worker.worker_toolset import WorkerToolset
import asyncio

LOW_DELAY = 0.1


class Worker:

    @classmethod
    def work(cls, toolset: WorkerToolset):
        page_url = toolset.get_next_page_url()
        get_request = GetRequest(toolset.proxies)
        get_request.no_retries = 5
        players_page = PlayersPage(page_url, get_request, toolset.use_proxy())
        players = players_page.get_players_ref_list()
        del players_page
        for player in players:
            get_request.send(player.href, toolset.use_proxy())
            if get_request.error_code == ErrorCode.HTTP_NOT_FOUND:
                print(get_request.error_msg)
                continue
            player.set_page_source(get_request.get_page_html_text())
            toolset.add_to_csv_queue(player)
            time.sleep(toolset.get_request_delay())
        del players


class Supervisor:

    def __init__(self, csv_logging_queue, config, start_page_no, last_page_no):
        self._worker_toolset = WorkerToolset(
            csv_logging_queue,
            PlayersPageUrlGenerator(start_page_no),
            config
        )
        self._no_pages_to_work = last_page_no - start_page_no + 1
        self._no_workers = config.get_no_working_threads()

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
