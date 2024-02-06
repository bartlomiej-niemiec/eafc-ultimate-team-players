import time
from concurrent.futures import ThreadPoolExecutor
from worker.worker import Worker
from worker.thread_safe_player_page import SafePlayersPageUrl

if __name__ == "__main__":
    NO_WORKERS = 5
    thread_pool = ThreadPoolExecutor(NO_WORKERS)
    page_url = SafePlayersPageUrl()
    future_workers = list(range(NO_WORKERS))

    work_start = time.time()
    for i in range(NO_WORKERS):
        future_workers[i] = thread_pool.submit(Worker.dig, page_url)

    for future in future_workers:
        future.result()

    print(f"We worked for {time.time() - work_start}s")
    print(f"We digged {NO_WORKERS} pages")