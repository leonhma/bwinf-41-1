from copy import deepcopy
from math import floor
from os import path
from time import time
from typing import Any, Callable, Iterable, List, Tuple
from pandas import DataFrame


start_time = 9*60
end_time = 17*60


def r_path(path_: str) -> str:
    """Return the absolute path to a file relative to the current file.

    Parameters
    ----------
    path_ : str
        The path to the file relative to the current file.

    Returns
    -------
    str
        The absolute path to the file.
    """
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


class TOD:
    """Time Of Day. Automatically jumps over the gaps in working time."""

    start_time: int
    end_time: int
    value: int

    def __init__(self, start_time: int, end_time: int):
        """Initialize the TOD.

        Parameters
        ----------
        start_time : int
            The time the working day starts in minutes from 00:00.
        end_time : int
            The time the working day ends in minutes from 00:00.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.value = start_time

    def get(self) -> int:
        """Return the current time.

        Returns
        -------
        int
            The current time in minutes.
        """
        return self.value

    def last_end(self) -> int:
        """Return the time the last timestep was finished.

        This only applies if an order is completed.

        Returns
        -------
        int
            The time the last timestep was finished at.
        """
        if self.value % (24*60) == self.start_time:
            days = floor(self.value // (24*60))
            return (days-1)*24*60+self.end_time
        return self.value

    def add(self, minutes: int):
        """Add minutes to the current time while accounting for gaps in
        working time.
        """
        days = minutes // (self.end_time - self.start_time)
        minutes_ = minutes % (self.end_time - self.start_time)
        self.set(self.value + days*24*60 + minutes_)

    def set(self, time: int):
        """Set the current time while accounting for gaps in working time."""
        days = floor(time / (24*60))
        minutes = time % (24*60)
        if minutes < self.start_time:
            self.value = days*24*60+self.start_time
        elif minutes >= self.end_time:
            self.value = (days+1)*24*60+self.start_time
        else:
            self.value = time


class Sim:
    """Simulate the processing of orders."""

    tod: TOD
    orders: Iterable[Tuple[int, int]]
    processing: List[List[int]]
    key: Callable[[Any], float]
    resumable: bool
    on_done: Callable[[int, int], None]

    def __init__(self, queue: Iterable[Tuple[int, int]], start_time: int, end_time: int):
        self.tod = TOD(start_time, end_time)    # create TOD object
        self.orders = deepcopy(queue)            # create a local copy of the orders queue
        self.orders.sort(key=lambda x: x[0])     # sort by submit
        self.processing = []
        self.key = lambda x: x[0]               # default sorting function for processing orders
        self.resumable = False                  # default to not resumable

    def __bool__(self) -> bool:
        # return true if there are still orders to process
        return bool(self.orders) or bool(self.processing)

    def set_key(self, key: Callable[[Any], float]):
        """Set the sorting key for which orders to prioritize.

        Parameters
        ----------
        key : Callable[[Any], float]
            A function that takes an order and returns a number that can be compared.
        """
        self.key = key

    def set_resumable(self, resumable: bool):
        """Set whether an order has to be completed first before another can be picked up.

        Parameters
        ----------
        resumable : bool
            Whether an order has to be completed first before another can be picked up.
        """
        self.resumable = resumable

    def set_callback(self, cb: Callable[[int, int], None]):
        """Set a callback for when an order is completed.

        Parameters
        ----------
        cb : Callable[[int, int], None]
            The callback to call withthe submit time and the end time of the
            order when it is finished.
        """
        self.on_done = cb

    def _update_processing(self):
        # move orders from orders to processing
        if len(self.processing) == 0 and self.orders:
            self.tod.set(self.orders[0][0])

        while self.orders and self.orders[0][0] <= self.tod.get():
            self.processing.append(list(self.orders.pop(0)))

    def run_until_end(self):
        """Run the simulation until all orders are processed.

        on_done is called for each order that is completed.
        """
        previous_order_done = True
        while self:
            self._update_processing()
            if self.resumable or previous_order_done:
                previous_order_done = False
                self.processing.sort(key=self.key)
            self.tod.add(1)
            self.processing[0][1] -= 1
            if self.processing[0][1] == 0:
                self.on_done(self.processing[0][0], self.tod.last_end())
                self.processing.pop(0)
                previous_order_done = True


def by_submit(orders: Iterable[Tuple[int, int]]) -> Tuple[int, float]:
    """Process orders in the order they were submitted and return the
    simulated wait times.

    Returns
    -------
    Tuple[int, float]
        [average wait time, maximum wait time]
    """
    avg_wait: float = 0
    n_avg_wait: int = 0
    max_wait: int = 0

    def on_done(submit: int, done: int):
        nonlocal avg_wait, n_avg_wait, max_wait
        wait = done - submit
        avg_wait = (n_avg_wait * avg_wait + wait) / (n_avg_wait + 1)
        n_avg_wait += 1
        max_wait = max(max_wait, wait)

    sim = Sim(orders, start_time, end_time)
    sim.set_key(lambda x: x[0])
    sim.set_resumable(False)
    sim.set_callback(on_done)

    sim.run_until_end()

    return max_wait, avg_wait


def by_duration(orders: Iterable[Tuple[int, int]]) -> Tuple[int, float]:
    """Process orders sorted by their duration and return the
    simulated wait times.

    Returns
    -------
    Tuple[int, float]
        [average wait time, maximum wait time]
    """
    avg_wait: float = 0
    n_avg_wait: int = 0
    max_wait: int = 0

    def on_done(submit: int, done: int):
        nonlocal avg_wait, n_avg_wait, max_wait
        wait = done - submit
        avg_wait = (n_avg_wait * avg_wait + wait) / (n_avg_wait + 1)
        n_avg_wait += 1
        max_wait = max(max_wait, wait)

    sim = Sim(orders, start_time, end_time)
    sim.set_key(lambda x: x[1])
    sim.set_resumable(False)
    sim.set_callback(on_done)

    sim.run_until_end()

    return max_wait, avg_wait


def by_duration_resumable(orders: Iterable[Tuple[int, int]]) -> Tuple[int, float]:
    """Process orders in the order they were submitted (resumable)
    and return the simulated wait times.

    Returns
    -------
    Tuple[int, float]
        [average wait time, maximum wait time]
    """
    avg_wait: float = 0
    n_avg_wait: int = 0
    max_wait: int = 0

    def on_done(submit: int, done: int):
        nonlocal avg_wait, n_avg_wait, max_wait
        wait = done - submit
        avg_wait = (n_avg_wait * avg_wait + wait) / (n_avg_wait + 1)
        n_avg_wait += 1
        max_wait = max(max_wait, wait)

    sim = Sim(orders, start_time, end_time)
    sim.set_key(lambda x: x[1])
    sim.set_resumable(True)
    sim.set_callback(on_done)

    sim.run_until_end()

    return max_wait, avg_wait


# main loop
def main():
    print()
    example_n = int(input('Bitte die Nummer des Beispiels eingeben [0; 4]: '))

    print()

    start_time = time()  # time measurement

    queue: List[Tuple[int]] = []  # [[submit, length]]
    with open(r_path(f'beispieldaten/fahrradwerkstatt{example_n}.txt'), 'r', encoding='utf-8') as f:
        for a, b in map(lambda x: tuple(map(int, x.split())),
                        filter(lambda x: x != '', f.read().split('\n'))):
            queue.append((a, b))

    processors = [by_submit, by_duration, by_duration_resumable]

    data = {processor.__name__: processor(queue)
            for processor in processors}   # apply all processors

    print(f'Aufträge simuliert in {format((time()-start_time)*1000, ".1f")}ms:')
    print()

    df = DataFrame(data, index=['Maximale Wartezeit (min)',
                   'Durchschnittliche Wartezeit (min)'])
    print(df.to_markdown(tablefmt='rounded_grid'))


# programmschleife
print('Fahrradwerkstatt')
print('(Drücke ^C um das Programm zu beenden)')

while True:
    try:
        main()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('\n')
        exit()
