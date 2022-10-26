from itertools import chain, permutations, product
from os import path
from functools import reduce
from operator import mul
from typing import Any, Iterator, List, Mapping, Tuple


def r_path(path_: str) -> str:
    return path.join(
        path.dirname(path.abspath(__file__)),
        path_
    )


def hash(board: Tuple[Tuple[int]]) -> Tuple[Tuple[int]]:
    """hash each block into an int to return a matrix of 3x3 ints"""
    def hash_block(board: Tuple[Tuple[int]], x: int, y: int) -> int:
        return (
            reduce(mul, (sum(1 if i != 0 else 0 for i in board[x*3+xo][y*3: y*3+3]) + 1 for xo in range(3))) +
            reduce(mul, (sum((1 if board[x*3+xo][y*3+yo] != 0 else 0)
                   for xo in range(3)) + 1 for yo in range(3)))
        )

    return tuple(
        tuple(
            hash_block(board, j, i)
            for j in range(3)
        )
        for i in range(3)
    )


def load_boards(path_: str) -> List[Tuple[Tuple[int]]]:
    """load boards from file"""
    with open(r_path(path_), 'r', encoding="utf-8-sig") as f:  # how come encoding is still a problem?
        return [
            tuple(
                tuple(
                    int(i) for i in line.split()
                ) for line in board.split('\n')
            ) for board in f.read().split('\n\n')
        ]


def boards_match(board1: Tuple[Tuple[int]],
                 board2: Tuple[Tuple[int]],
                 xmapping: List[int],
                 ymapping: List[int]) -> Mapping[int, int]:
    """check if two boards are identical except for swapped numbers. return number mapping if they are"""
    number_mapping = {0: 0}
    for x in range(9):
        for y in range(9):
            if board1[xmapping[x]][ymapping[y]] in number_mapping:
                if number_mapping[board1[xmapping[x]][ymapping[y]]] != board2[x][y]:
                    return
            else:
                number_mapping[board1[xmapping[x]][ymapping[y]]] = board2[x][y]
    else:
        return number_mapping


def rotations(board: Tuple[Tuple[int]]) -> Iterator[Tuple[int, Tuple[Tuple[int]]]]:
    """iterate through all rotations of a board"""
    current = board
    yield (0, current)
    for i in range(1, 4):
        current = tuple(zip(*current[::-1]))
        yield (i, current)


def boards_similar(board1: Tuple[Tuple[int]], board2: Tuple[Tuple[int]]) -> Mapping[str, Any]:
    """check if two boards are similar"""
    board2hash = hash(board2)

    for xdivmapping in permutations(range(3)):
        for ydivmapping in permutations(range(3)):
            for rot, board1rot in rotations(board1):
                board1hash = hash(board1rot)
                if all(
                    board1hash[xdivmapping[x]][ydivmapping[y]] == board2hash[x][y]
                    for x in range(3) for y in range(3)
                ):
                    # rough hashes match
                    for xcolmappings in product(*(permutations(range(3)) for _ in range(3))):
                        xmapping = tuple(
                            chain(
                                *
                                (tuple(map(lambda x: x + i * 3, xcolmappings[i]))
                                 for i in xdivmapping)))
                        for yrowmappings in product(*(permutations(range(3)) for _ in range(3))):
                            ymapping = tuple(
                                chain(
                                    *
                                    (tuple(map(lambda x: x + i * 3, yrowmappings[i]))
                                     for i in ydivmapping)))
                            if number_mapping := boards_match(
                                    board1rot, board2, xmapping, ymapping):
                                return {
                                    'xdivmapping': xdivmapping,
                                    'ydivmapping': ydivmapping,
                                    'xcolmappings': xcolmappings,
                                    'yrowmappings': yrowmappings,
                                    'rotation': rot,
                                    'number_mapping': number_mapping
                                }
    else:
        return False


def fprint_solution(solution: Mapping):
    """print human-readable solution"""
    if solution['xdivmapping'] != (0, 1, 2):
        print(
            f"- Vertauschung der Zeilenblöcke: {', '.join(f'{i+1} -> {t+1}' for i, t in enumerate(solution['xdivmapping']) if i != t)}")
    if solution['ydivmapping'] != (0, 1, 2):
        print(
            f"- Vertauschung der Spaltenblöcke: {', '.join(f'{i+1} -> {t+1}' for i, t in enumerate(solution['ydivmapping']) if i != t)}")
    if solution['rotation'] != 0:
        print(f"- Drehung im Uhrzeigersinn um {solution['rotation']*90}°")

    if solution['xcolmappings'] != ((0, 1, 2), (0, 1, 2), (0, 1, 2)):
        print(
            f"- Vertauschen der Zeilen: {', '.join(f'{m*3+1+i} -> {m*3+1+t}' for m, mapping in enumerate(solution['xcolmappings']) for i, t in enumerate(mapping) if i != t)}")
    if solution['yrowmappings'] != ((0, 1, 2), (0, 1, 2), (0, 1, 2)):
        print(
            f"- Vertauschen der Spalten: {', '.join(f'{m*3+1+i} -> {m*3+1+t}' for m, mapping in enumerate(solution['yrowmappings']) for i, t in enumerate(mapping) if i != t)}")
    if any(i != t for i, t in solution['number_mapping'].items()):
        print(
            f"- Umbenennung der Zahlen: {', '.join(f'{i} -> {t}' for i, t in solution['number_mapping'].items() if i != t)}")


# loop
while True:
    try:
        number = input('Nummer des Beispiels eingeben [0; 4]: ')
        print()
        board1, board2 = load_boards(f'beispieldaten/sudoku{number}.txt')
        if solution := boards_similar(board1, board2):
            print('Die beiden Sudokus sind ähnlich!')
            fprint_solution(solution)
        else:
            print('Die beiden Sudokus sind nicht ähnlich.')
    except Exception as e:
        print(f'Fehler: {e}')
    except KeyboardInterrupt:
        print()
        exit()
    print()
