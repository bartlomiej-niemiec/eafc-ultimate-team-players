from concurrent.futures import ThreadPoolExecutor
from worker.worker import Worker
from worker.thread_safe_player_page import SafePlayersPageUrl
import asyncio

PAGES_TO_DIG = 10


async def get_work_done():
    page_url = SafePlayersPageUrl()
    with ThreadPoolExecutor(max_workers=5) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                Worker.dig,
                page_url
            )
            for i in range(PAGES_TO_DIG)
        ]

    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_work_done())
    loop.run_until_complete(future)
