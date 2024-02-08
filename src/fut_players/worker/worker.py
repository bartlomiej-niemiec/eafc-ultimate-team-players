import time
from utils.constants import NO_WORKERS
from concurrent.futures import ThreadPoolExecutor
from futwiz.players_page.futwiz_players_page import PlayersPage
from futwiz.player_page.futwiz_concrete_player_page import PlayerPage
from fut_players.worker.worker_toolset import WorkerToolset
import asyncio


class Worker:

    @classmethod
    def work(cls, toolset: WorkerToolset):
        page_url = toolset.get_next_page_url()
        players_page = PlayersPage(page_url)
        players = players_page.get_players_ref_list()
        for player in players:
            player_page = PlayerPage(player.href)
            player_data = player_page.get_player_data()
            toolset.logging_queue.put(player_data)
            toolset.page_complete_monitor.increment()
            time.sleep(toolset.request_delay)


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
