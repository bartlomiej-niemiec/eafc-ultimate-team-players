import time
from threading import Thread, Event
import csv

LOGGER_THREAD_DELAY = 0.2
ALT_POS_KEY = 'Alt Pos.'


class Logger(Thread):

    def __init__(self, shared_queue):
        super(Logger, self).__init__()
        self.shared_queue = shared_queue
        self._stop_event = Event()
        self._csv_dictwriter = None

    def run(self):
        self._logger()

    def stop(self):
        self._stop_event.set()
        while not self.shared_queue.empty():
            queue_object = self.shared_queue.get()
            self._csv_dictwriter.writerow(queue_object)

    def _logger(self):
        queue_object = None
        is_first_log = True
        with open('fut_players.csv', 'w', newline='', encoding="utf-8") as csvfile:
            while True:
                if self._stop_event.isSet():
                    break
                if not self.shared_queue.empty():
                    queue_object = self.shared_queue.get()
                    self._add_alt_pos_if_is_missing(queue_object)
                    if is_first_log:
                        self._first_save(csvfile, queue_object)
                        is_first_log = False
                    self._csv_dictwriter.writerow(queue_object)
                time.sleep(LOGGER_THREAD_DELAY)

    def _first_save(self, csvfile, object):
        self._csv_dictwriter = csv.DictWriter(csvfile, fieldnames=object.keys())
        self._csv_dictwriter.writeheader()

    def _add_alt_pos_if_is_missing(self, object):
        alt_pos = object.get(ALT_POS_KEY)
        if not alt_pos:
            object[ALT_POS_KEY] = None
