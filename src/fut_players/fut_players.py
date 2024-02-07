from fut_players.worker import Worker
from concurrent.futures import ThreadPoolExecutor
import asyncio


def fut_players_runner(page_url_generator, delay, pages, logging_queue, page_complete_monitor):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_work_done(page_url_generator, delay, pages, logging_queue, page_complete_monitor))
    loop.run_until_complete(future)


async def get_work_done(page_url_generator, delay, pages, logging_queue, page_complete_monitor):
    with ThreadPoolExecutor(max_workers=5) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                Worker.work,
                page_url_generator,
                delay,
                logging_queue,
                page_complete_monitor
            )
            for _ in range(pages)
        ]

    return await asyncio.gather(*tasks)
