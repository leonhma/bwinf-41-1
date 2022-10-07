from dataclasses import dataclass, field
from heapq import heapify, heappop, heappush
from typing import Any, Callable, List, Mapping, Tuple
from os import path


def rel_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


# 1-based ilist for distance matrix
class ilist(list):
    def __init__(self, r=None, dft: Callable[[], Any] = None):
        if r is None:
            r = []
        list.__init__(self, r)
        self.dft = dft

    def _ensure_length(self, n):
        maxindex = n
        if isinstance(maxindex, slice):
            maxindex = maxindex.indices(len(self))[1]
        while len(self) <= maxindex:
            self.append(self.dft())

    def __getitem__(self, n):
        self._ensure_length(n-1)
        return super(ilist, self).__getitem__(n-1)

    def __setitem__(self, n, val):
        self._ensure_length(n-1)
        return super(ilist, self).__setitem__(n-1, val)


class LLVertice:
    def __init__(self, value: int, previous=None):
        self.value = value
        self.previous = previous


@dataclass
class AStarItem:
    d_source: int = field(compare=False)
    d_target: int = field(compare=False)

    path: LLVertice = field(compare=False)

    @property
    def priority(self):
        return self.d_source + self.d_target

    def __lt__(self, other):
        return self.priority < other.priority

def get_path(vertice: LLVertice) -> List[int]:
    path = []
    while vertice is not None:
        path.append(vertice.value)
        vertice = vertice.previous
    return path[::-1]


def compute_distances(graph: Mapping[int, List[int]]) -> List[List[int]]:
    distances: List[List[float]] = ilist(dft=lambda: ilist(dft=lambda: float('inf')))

    for start in range(1, len(graph)):
        distances[start][start] = 0
        seen = set()
        q = [start]
        while len(q) > 0:
            current = q.pop(0)
            seen.add(current)
            if current in graph:
                for next_ in graph[current]:
                    if next_ not in seen:
                        distances[start][next_] = distances[start][current] + 1
                        q.append(next_)
    return distances


def check_match(heap1: List[AStarItem], heap2: List[AStarItem]) -> Tuple[List[int], List[int]] or False:
    for item1 in heap1:
        for item2 in heap2:
            if item1.path.value == item2.path.value and item1.d_source == item2.d_source:
                return get_path(item1.path), get_path(item2.path)
    return False


def get_meeting_point(graph: Mapping[int, List[int]],
                      v1: int, v2: int) -> Tuple[List[int],
                                                 List[int]] or False:
    if v1 == v2:
        return [v1], [v2]

    distances = compute_distances(graph)

    v1target = v2
    v1heap = [AStarItem(0, distances[v1][v1target], LLVertice(v1))]
    heapify(v1heap)
    v1min_d = distances[v1][v2]
    v2target = v1
    v2heap = [AStarItem(0, distances[v2][v2target], LLVertice(v2))]
    heapify(v2heap)
    v2min_d = distances[v2][v1]

    n_of_steps_wo_progress = 200  # stop after 20 steps w/o getting closer to the target

    while n_of_steps_wo_progress > 0:
        print(f'step {v1target=}: {v1min_d=}, {v2target=}: {v2min_d=}')
        # if one is empty, return false
        if len(v1heap) == 0 or len(v2heap) == 0:
            return False

        asitem = heappop(v1heap)
        v2target = asitem.path.value
        if asitem.d_target < v1min_d:
            v1min_d = asitem.d_target
            n_of_steps_wo_progress = 200
        else:
            n_of_steps_wo_progress -= 1

        for next_ in graph[asitem.path.value]:
            heappush(
                v1heap, AStarItem(
                    asitem.d_source + 1, distances[next_][v1target],
                    LLVertice(next_, asitem.path)))

        if res := check_match(v1heap, v2heap):
            return res

        asitem = heappop(v2heap)
        v1target = asitem.path.value
        if asitem.d_target < v2min_d:
            v2min_d = asitem.d_target
            n_of_steps_wo_progress = 200
        else:
            n_of_steps_wo_progress -= 1
        for next_ in graph[asitem.path.value]:
            heappush(
                v2heap, AStarItem(
                    asitem.d_source + 1, distances[next_][v2target],
                    LLVertice(next_, asitem.path)))
        
        if res := check_match(v1heap, v2heap):
            return res

    else:
        return False


# programmschleife
print('Hüpfburg')
print('(Drücke ^C um das Programm zu beenden)')

while True:
    print()
    bsp_nr = int(input('Bitte die Nummer des Beispiels eingeben [0; 4]: '))

    print()

    graph: Mapping[int, List[int]] = {}

    with open(rel_path(f'beispieldaten/huepfburg{bsp_nr}.txt'), 'r') as f:
        f.readline()  # skip first line
        while line := f.readline().strip():
            a, b = map(int, line.split())
            if a in graph:
                graph[a].append(b)
            else:
                graph[a] = [b]

    print(get_meeting_point(graph, 1, 2))
