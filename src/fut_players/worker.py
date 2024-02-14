import time
from futwiz.players_page_generator import PlayersPageUrlGenerator
from concurrent.futures import ThreadPoolExecutor
from futwiz.players_page_parser import PlayersPageParser
from utils.get_requests import GetRequest, ErrorCode
from fut_players.worker_toolset import WorkerToolset
import asyncio
import config

LOW_DELAY = 0.1


class Worker:

    @classmethod
    def work(cls, toolset: WorkerToolset):
        page_url = toolset.get_next_page_url()
        get_request = GetRequest(toolset.proxies)
        get_request.no_retries = config.MAX_RETRIES
        get_request.delay = config.DELAY_BETWEEN_TO_RETRY
        get_request.send(page_url, toolset.use_proxy())
        players_page = PlayersPageParser(get_request.get_page_html_text())
        players = players_page.get_players_ref_list()
        del players_page
        for player in players:
            get_request.send(player.href, toolset.use_proxy())
            if get_request.error_code == ErrorCode.HTTP_NOT_FOUND:
                print(get_request.error_msg)
                continue
            elif get_request.get_page_html_text() is None:
                print(
                    f"""Failed to get source for player: {player.href}
                        Error code: {get_request.error_code}
                        Error msg: {get_request.error_msg}"""
                      )
                continue
            player.page_source(get_request.get_page_html_text())
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
