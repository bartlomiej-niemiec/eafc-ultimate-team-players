import asyncio
from concurrent.futures import ThreadPoolExecutor

import config
from fut_players.common.page_visitor import Toolset, PageVisitor
from futwiz.players_page.players_page_url_generator import PlayerPageUrlFactory
from futwiz.players_page.util import PlayersPageType


class FutPlayersSupervisor:

    def __init__(self, csv_logging_queue, start_page_no, last_page_no):
        self._worker_toolset = Toolset(
            csv_logging_queue,
            PlayerPageUrlFactory.create(start_page_no, PlayersPageType.AllPlayers),
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
                    PageVisitor.work,
                    self._worker_toolset
                )
                for _ in range(self._no_pages_to_work)
            ]

        return await asyncio.gather(*tasks)
