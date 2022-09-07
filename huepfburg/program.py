from time import time
from os import path
from typing import Generator, List, Mapping, Tuple
from collections import deque


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


def shortest_path(a: int, b: int, graph: Mapping[int, List[int]]) -> Tuple[int, Tuple[int, ...]]:
    unseen = set(graph.keys())

    q = deque((a, []))

    while q:
        current, currentpath = q.popleft()
        if current == b:
            return len(currentpath), tuple(currentpath)
        if current not in unseen:
            continue
        unseen.remove(current)
        for next_ in graph[current]:
            q.append(next_, currentpath + [next_])
    return False


# hauptprogramm
def main():
    print()
    bsp_nr = int(input('Bitte die Nummer des Beispiels eingeben [0; 4]: '))

    print()

    start_time = time()  # variable für die zeitmessung

    # laden des graphen mit umgedrehten pfeilen um memoization zu erleichtern
    graph: Mapping[int, List[int]]
    with open(r_path(f'beispieldaten/huepfburg{bsp_nr}.txt'), 'r') as f:
        n, m = map(int, f.readline().split())
        graph = {i: [] for i in range(1, n + 1)}
        for a, b in map(lambda x: map(int, x.split()), f.readlines()[:m]):
            graph[a].append(b)

    unseen = set(graph.keys())
    





# programmschleife
print('Hüpfburg')
print('(Drücke ^C um das Programm zu beenden)')

while True:
    try:
        main()
    # except Exception as e:
    #     print(e)
    except KeyboardInterrupt:
        print('\n')
        exit()
