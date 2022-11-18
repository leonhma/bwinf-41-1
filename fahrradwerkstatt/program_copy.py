from copy import deepcopy
from enum import Enum
from math import floor
from queue import PriorityQueue
from time import time
from os import path
from typing import Any, Callable, List, Tuple
from pandas import DataFrame
from contextlib import suppress

work_start = 9*60  # work start, minutes from 0:00
work_end = 17*60  # work end, minutes from 0:00

# relativer pfad zu speicherplatz der aktuellen datei


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


class EventType(Enum):
    WORK_END = 0
    NEW_ORDER = 1
    CURRENT_DONE = 2


class TOD:
    """Time Of Day. Automatically jumps over the gaps in working time"""
    start_time: int
    end_time: int
    time: int

    def __init__(self, start_time, end_time):
        self.time = self.start_time = start_time
        self.end_time = end_time

    def __add__(self, minutes: int) -> 'TOD':
        if (self.time % (24*60) + minutes % (8*60)) < self.end_time:
            self.time += minutes
        else:
            self.time += minutes + ((24*60-work_end)+work_start)
        return self

    def set(self, time: int):
        days = floor(time / (24*60))
        tod = time % (24*60)
        if tod < 9*60:
            self.time = days*24*60+9*60
        elif tod >= 17*60:
            self.time = (days+1)*24*60+9*60+tod-17*60
        else:
            self.time = time

    def __int__(self):
        return self.time


class OrdersQueue:
    time: TOD
    orders: List[Tuple[int]]  # Tuples of orders from the future (submit, time)
    processing: List[List[int]]
    priority: Callable = lambda x: x[0]  # sorting function for processing orders
    on_done: Callable[[int, int], None]

    def __init__(self, orders: List[Tuple[int, int]], start_time: int, end_time: int):
        self.orders = sorted(deepcopy(orders), key=lambda x: x[0])  # sort by submit
        self.processing = []
        self.time = TOD(start_time, end_time)

    def __bool__(self) -> bool:
        return (bool(self.orders) or bool(self.processing))

    def on_done(self, cb: Callable):
        """Set a callback for when an order is completed."""
        self.on_done = cb

    def set_priority(self, key: Callable[[Any], int]):
        """Set the sorting key for which orders to prioritize."""
        self.priority = key

    def _update_processing(self):
        """Update list of considered orders."""
        with suppress(IndexError):
            while self.orders[0][0] <= int(self.time):
                self.processing.append(list(self.orders.pop(0)))

        with suppress(IndexError):
            if len(self.processing) == 0:
                self.processing.append(self.orders.pop(0))
                self.time.set(self.processing[0][0])

        self.processing.sort(key=self.priority)

    def _time_until_next_event(self) -> Tuple[int, EventType]:
        # assumed: work_start <= self.time <= work_end
        ttno = self.orders[0][0] - int(self.time) if len(self.orders) else 9999999999  # time-to-new-order
        tteow = work_end - (int(self.time) % (24*60))  # time-to-end-of-work

        return min([(ttno, EventType.NEW_ORDER),
                   (tteow, EventType.WORK_END),
                   (self.processing[0][1], EventType.CURRENT_DONE)])

    def work(self, time: int):
        # work (assumes currently working hours)
        time_worked = 0
        while time_worked < time:
            self._update_processing()
            t_, _ = self._time_until_next_event()
            t = min(t_, time-time_worked)
            time_worked += t
            self.time += t
            self.processing[0][1] -= t
            if self.processing[0][1] < 0:
                print(f'{self.processing[0][1]=}')
                exit()
            if self.processing[0][1] == 0:
                self.on_done(self.processing[0][0], self.time.time)
                self.processing.pop(0)
                if not self.processing and not self.orders:
                    return

    def work_until_next_order_submit(self):
        self._update_processing()
        while True:
            # add end condition
            t, e = self._time_until_next_event()
            self.work(t)
            if e == EventType.NEW_ORDER:
                return
            self._update_processing()
            if not self.orders and not self.processing:
                return


# bearbeitungsmethode: nach einreichungszeit sortiert
def by_submit(orders: List[Tuple[int, int]]) -> Tuple[int, int]:
    global max_wait, avg_wait, n_avg_wait
    q = OrdersQueue(orders, work_start, work_end)

    max_wait = 0

    avg_wait = 0
    n_avg_wait = 0

    def order_done(submit: int, finish: int):
        global max_wait, avg_wait, n_avg_wait
        wait = finish-submit
        max_wait = max(max_wait, wait)
        avg_wait = (n_avg_wait * avg_wait + wait) / (n_avg_wait + 1)
        n_avg_wait += 1

    q.on_done(order_done)
    q.set_priority(lambda x: x[0])

    while q:
        q.work(24*60)

    return max_wait, avg_wait


# bearbeitungsmethode: nach bearbeitungszeit sortiert
def by_duration(queue: List[List[int]]) -> Tuple[int, int]:
    p = PriorityQueue()
    done = 0

    max_wait = 0

    avg_wait = 0
    n_avg_wait = 0

    for i, (submit, duration) in enumerate(queue):
        done = max(done, submit)
        p.put((duration, submit))
        while not p.empty() and (i + 1 == len(queue) or done < queue[i + 1][0]):
            duration, submit = p.get(block=False, timeout=0)
            wait = max(0, done - submit) + duration
            done = done+duration

            max_wait = max(max_wait, wait)
            avg_wait = (n_avg_wait * avg_wait + wait) / (n_avg_wait + 1)
            n_avg_wait += 1

    return max_wait, avg_wait


# bearbeitungsmethode: nach bearbeitungszeit sortiert mit wiederaufnehmbarkeit
def by_duration_resumable(queue: List[List[int]]) -> Tuple[int, int]:
    p = PriorityQueue()

    max_wait = 0

    avg_wait = 0
    n_avg_wait = 0

    done = 0

    for i, (submit, duration) in enumerate(queue):
        done = max(done, submit)
        p.put((duration, submit))
        next_submit = queue[i + 1][0] if i + 1 < len(queue) else 9999999999999999
        while not p.empty() and done < next_submit:
            duration, submit = p.get(block=False, timeout=0)
            if duration > next_submit - done:
                p.put((duration - (next_submit - done), submit))
                done = next_submit
                break
            done = done+duration
            wait = done - submit

            max_wait = max(max_wait, wait)
            avg_wait = (n_avg_wait * avg_wait + wait) / (n_avg_wait + 1)
            n_avg_wait += 1

    return max_wait, avg_wait


# hauptprogramm
def main():
    print()
    bsp_nr = int(input('Bitte die Nummer des Beispiels eingeben [0; 4]: '))

    print()

    start_time = time()  # variable für die zeitmessung

    queue: List[List[int]] = []  # [[submit, length]]
    with open(r_path(f'beispieldaten/fahrradwerkstatt{bsp_nr}.txt'), 'r') as f:
        for a, b in map(lambda x: tuple(map(int, x.split())),
                        filter(lambda x: x != '', f.read().split('\n'))):
            queue.append([a, b])

    queue.sort()

    processors = [by_submit, by_duration, by_duration_resumable]

    data = {processor.__name__: processor(queue) for processor in processors}

    df = DataFrame(data, index=['Maximale Wartezeit (min)',
                   'Durchschnittliche Wartezeit (min)'])

    print(f'Aufträge simuliert in {format(time()-start_time, ".3f")}ms:')
    print()
    print(df.to_markdown(tablefmt='fancy_grid', floatfmt='.3f'))


# programmschleife
print('Fahrradwerkstatt')
print('(Drücke ^C um das Programm zu beenden)')

while True:
    main()
