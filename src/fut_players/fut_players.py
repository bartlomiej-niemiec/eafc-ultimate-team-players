from fut_players.worker import Worker
from concurrent.futures import ThreadPoolExecutor
import asyncio


def fut_players_runner(worker_toolset, no_pages):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_work_done(worker_toolset, no_pages))
    loop.run_until_complete(future)


async def get_work_done(worker_toolset, no_pages):
    with ThreadPoolExecutor(max_workers=5) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                Worker.work,
                worker_toolset
            )
            for _ in range(no_pages)
        ]

    return await asyncio.gather(*tasks)
