from typing import List, Mapping, Tuple
from time import time
from os import path


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


# linked list for keeping track of the path so far
class LLVertice:
    def __init__(self, value: int, previous=None):
        self.value = value
        self.previous = previous


def get_path(vertice: LLVertice) -> List[int]:
    path = []
    while vertice is not None:
        path.append(vertice.value)
        vertice = vertice.previous
    return path[::-1]


def get_meeting_point(graph: Mapping[int, int],
                      v1: int, v2: int) -> Tuple[List[int],
                                                 List[int]] or False:
    if v1 == v2:
        return [v1], [v2]

    start_time_sdf = time()
    distances: Mapping[int, Mapping[int, int]] = {}

    for start in graph:
        distances[start] = {start: 0}
        q = [start]
        while len(q) > 0:
            current = q.pop(0)
            if current in graph:
                for next_ in graph[current]:
                    if next_ not in distances[start]:
                        distances[start][next_] = distances[start][current] + 1
                        q.append(next_)

    print(f'calculated distances in {format(time()-start_time_sdf, ".3f")}s')
    return

    v1q, v2q = [LLVertice(v1)], [LLVertice(v2)]
    # v1seen, v2seen = set(), set()

    for _ in range(1000):
        # if one is empty, return false
        if len(v1q) == 0 or len(v2q) == 0:
            return False

        # go through one iteration of next vertices
        # v1stuck = True
        for _ in range(len(v1q)):
            current = v1q.pop(0)
            # if current.value not in v1seen:
            #     v1stuck = False
            #     v1seen.add(current.value)
            if current.value in graph:
                for next_ in graph[current.value]:
                    v1q.append(LLVertice(next_, current))

        v1qh = {x.value: x for x in v1q}

        # v2stuck = True
        for _ in range(len(v2q)):
            current = v2q.pop(0)
            # if current.value not in v2seen:
            #     v2stuck = False
            #     v2seen.add(current.value)
            if current.value in graph:
                for next_ in graph[current.value]:
                    if next_ in v1qh:
                        return get_path(v1qh[next_]), get_path(LLVertice(next_, current))
                    v2q.append(LLVertice(next_, current))

        print(f'length of v1q is {len(v1q)}, length of v2q is {len(v2q)}')
        # print(f'stuck values: {v1stuck=}, {v2stuck=}')
        # if v1stuck and v2stuck:
        #     print('detected stuck condition. returning')
        #     return False


# programmschleife
print('Hüpfburg')
print('(Drücke ^C um das Programm zu beenden)')

while True:
    print()
    bsp_nr = int(input('Bitte die Nummer des Beispiels eingeben [0; 4]: '))

    print()

    start_time = time()  # variable für die zeitmessung

    graph: Mapping[int, List[int]] = {}

    with open(r_path(f'beispieldaten/huepfburg{bsp_nr}.txt'), 'r') as f:
        f.readline()  # skip first line
        while line := f.readline().strip():
            a, b = map(int, line.split())
            if a in graph:
                graph[a].append(b)
            else:
                graph[a] = [b]

    print(f'Graph geladen in {format(time()-start_time, ".3f")}ms:')

    print()

    start_time = time()  # variable für die zeitmessung

    if res := get_meeting_point(graph, 1, 2):
        print(f'Pfad gefunden in {format(time()-start_time, ".3f")}ms:')
        print()
        print(f"Pfad 1: {' -> '.join(map(str, res[0]))}")
        print(f"Pfad 2: {' -> '.join(map(str, res[1]))}")

    # except KeyboardInterrupt:
    #     print('\n')
    #     exit()
