import time
from utils.constants import NO_WORKERS
from concurrent.futures import ThreadPoolExecutor
from futwiz.players_page.futwiz_players_page import PlayersPage
from utils.get_requests import get_request_with_retries
from fut_players.worker.worker_toolset import WorkerToolset
import asyncio

LOW_DELAY = 0.1


class Worker:

    @classmethod
    def work(cls, toolset: WorkerToolset):
        page_url = toolset.get_next_page_url()
        players_page = PlayersPage(page_url, toolset.proxies, False)
        players = players_page.get_players_ref_list()
        del players_page
        for player in players:
            player_page_text = get_request_with_retries(player.href, 5, False, toolset.proxies)
            if not player_page_text:
                print(f"Error for url: {player.href}")
                continue
            player.set_page_source(player_page_text)
            toolset.add_to_csv_queue(player)
            time.sleep(toolset.request_delay)
        del players


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
