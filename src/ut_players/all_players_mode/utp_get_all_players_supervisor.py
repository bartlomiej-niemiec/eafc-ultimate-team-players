import asyncio
from concurrent.futures import ThreadPoolExecutor
from ut_players.common.page_visitor import PageVisitor


class UtpGetAllPlayerSupervisor:

    def __init__(self, no_pages, no_threads, toolset):
        self._worker_toolset = toolset
        self._no_pages_to_work = no_pages
        self._no_workers = no_threads

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
