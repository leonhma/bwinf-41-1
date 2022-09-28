from queue import PriorityQueue
from time import time
from os import path
from typing import List, Tuple
from pandas import DataFrame


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


def by_submit(queue: List[Tuple[int, int]]) -> Tuple[int, int]:
    queue.sort(key=lambda x: x[0])
    done = 0

    max_wait = 0

    avg_wait = 0
    n_avg_wait = 0

    for submit, duration in queue:
        wait = max(0, done - submit) + duration
        done = max(done, submit)+duration

        max_wait = max(max_wait, wait)
        avg_wait = (n_avg_wait * avg_wait + wait) / (n_avg_wait + 1)
        n_avg_wait += 1

    return max_wait, avg_wait


def by_duration(queue: List[Tuple[int, int]]) -> Tuple[int, int]:
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


def by_duration_resumable(queue: List[Tuple[int, int]]) -> Tuple[int, int]:
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

    # laden des graphen mit umgedrehten pfeilen um memoization zu erleichtern
    queue: List[Tuple[int, int]] = []
    with open(r_path(f'beispieldaten/fahrradwerkstatt{bsp_nr}.txt'), 'r') as f:
        for a, b in map(lambda x: tuple(map(int, x.split())),
                        filter(lambda x: x != '', f.read().split('\n'))):
            queue.append((a, b))

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
    try:
        main()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('\n')
        exit()
