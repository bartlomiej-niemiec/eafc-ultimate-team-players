from utils.constants import NO_WORKERS
from fut_players.worker.worker import Worker
from concurrent.futures import ThreadPoolExecutor
import asyncio


def start_work(worker_toolset, no_pages_to_work_on):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(_get_work_done(worker_toolset, no_pages_to_work_on))
    loop.run_until_complete(future)


async def _get_work_done(worker_toolset, no_pages_to_work_on):
    with ThreadPoolExecutor(max_workers=NO_WORKERS) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                Worker.work,
                worker_toolset
            )
            for _ in range(no_pages_to_work_on)
        ]

    return await asyncio.gather(*tasks)
